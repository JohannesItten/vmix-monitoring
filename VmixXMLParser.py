import xmltodict
import VmixInput as VmixInput
import VmixBus as VmixBus
import VmixGlobal as VmixGlobal


class VmixXMLParser:
    XML_ROOT = 'vmix'
    #common XML element names for all vMix projects
    #except inputs, buses, overlays
    GLOBALS = ['version',
                'edition',
                'streaming',
                'recording',
                'external',
                'playList',
                'multiCorder',
                'fullscreen',
                'preview',
                'active'
                ]

    BUSES_ROOT = 'audio'
    INPUTS_ROOT = 'inputs'
    OVERLAYS_ROOT = 'overlays'

    LAST_OVERLAY_NUMBER = 4 #cause overlays 5-8 - stingers


    def __init__(self, xml, keys=[]):
        self.xml = xml
        self.json = xmltodict.parse(xml)[self.XML_ROOT]
        self.keys = keys


    def parse(self) -> dict:
        vmix_global = self.get_global_elements()
        buses = self.get_buses()
        active_input_number = vmix_global.get_value("active")
        active_input = self.get_input(active_input_number)
        needed_inputs = self.get_needed_inputs()
        overlays = self.get_used_overlays()
        
        result = {
            "global": vmix_global,
            "buses": buses,
            "active": active_input,
            "needed": needed_inputs,
            "overlays": overlays
        }
        return result


    #get xml element properties
    #blah-blah about xmltodict
    def get_element_properties(self, state) -> dict:
        props = {}
        for prop in state:
            if '@' not in prop:
                continue
            if not prop[1:].isalpha():
                prop_name = prop[1:-1]
                prop_number = prop[-1]
                if (prop_name not in props):
                    props[prop_name] = {} 
                props[prop_name][prop_number] = (state[prop])
                continue
            props[prop[1:]] = state[prop]
        return props


    def get_input_overlays(self, input) -> list:
        input_overlays = []
        if not "overlay" in input: return []
        for overlay in input["overlay"]:
            input_overlays.append(overlay[
                "@key"])
        return input_overlays


    def get_input_texts(self, input) -> dict:
        input_texts = {}
        if not "text" in input: return {}
        for text in input["text"]:
            text_name = text['@name']
            input_texts[text_name] = text["#text"]
        return input_texts


    #get common elements properties and state
    def get_global_elements(self) -> VmixGlobal:
        globals = {}
        globals_names = self.GLOBALS
        state = self.json
        
        for name in globals_names:
            if name not in state:
                continue
            value = state[name]
            if type(value) is not str:
                value = value["#text"]
            globals[name] = {
                "value": value,
                "props": self.get_element_properties(state[name])
            }

        global_obj = VmixGlobal.VmixGlobal(globals) 
        return global_obj



    def get_buses(self) -> list:
        buses = []
        root = self.BUSES_ROOT
        state = self.json

        for bus in state[root]:
            bus_props = self.get_element_properties(state[root][bus])
            buses.append(VmixBus.VmixBus(
                name=bus,
                is_muted=eval(bus_props["muted"]),
                volume_bar=float(bus_props["volume"]),
                props=bus_props
            ))
        return buses
    

    #it works due to inputs always sorted by input number
    def get_input(self, input_number: int=-1) -> VmixInput:
        if input_number <= 0: return []
        state = self.json
        inputs = state[self.INPUTS_ROOT]["input"]
        input = inputs[input_number - 1]        

        input_obj = VmixInput.VmixInput(
            number=input_number,
            key=input['@key'],
            title=input['@title'],
            overlays=self.get_input_overlays(input),
            texts=self.get_input_texts(input),
            props=self.get_element_properties(input)
        )
        return input_obj


    #inputs which we need to mon, found by user defined keys
    def get_needed_inputs(self) -> list:
        needed_inputs = []
        state = self.json
        keys = self.keys

        inputs = state[self.INPUTS_ROOT]["input"]
        for input in inputs:
            input_title = input["@title"]
            input_number = input["@number"]

            if any(el in input_title for el in keys):
                inputObj = VmixInput.VmixInput(
                    number=input_number,
                    key=input["@key"],
                    title=input_title,
                    overlays=self.get_input_overlays(input),
                    texts=self.get_input_texts(input),
                    props=self.get_element_properties(input)
                )
                needed_inputs.append(inputObj)
        return needed_inputs


    #inputs info got same way as get_active_input
    def get_used_overlays(self) -> dict:
        used_overlays = {}
        state = self.json

        inputs = state[self.INPUTS_ROOT]["input"]
        for overlay in state[self.OVERLAYS_ROOT]["overlay"]:
            if not "#text" in overlay: continue
            input_number = int(overlay["#text"])
            print(input_number)
            used_overlays[overlay["@number"]] = self.get_input(input_number)
            if int(overlay["#text"]) == self.LAST_OVERLAY_NUMBER: break 
        return used_overlays