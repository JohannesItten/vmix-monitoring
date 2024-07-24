import xmltodict

#state = snapshot of vMix XML API
#element = streaming, recording, preview, active, etc. 
#properties = streaming channel, meterF1, etc.

class VmixXMLParser:
    XML_ROOT = 'vmix'
    #common XML element names for all vMix projects
    #except inputs, buses, overlays
    COMMONS = ['version',
                'edition'
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
        commons = self.get_common_elements()
        buses = self.get_buses()
        active_input = self.get_active_input(int(commons["active"]["state"]))
        needed_inputs = self.get_needed_inputs()
        overlays = self.get_used_overlays()
        
        result = {
            "commons": commons,
            "buses": buses,
            "active": active_input,
            "needed": needed_inputs,
            "overlays": overlays
        }
        return result


    #get element properties
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


    #get common elements properties and state
    def get_common_elements(self) -> dict:
        commons = {}
        commons_names = self.COMMONS
        state = self.json
        
        for name in commons_names:
            if name not in state:
                continue
            commons[name] = {
                "state": state[name],
                "properties": self.get_element_properties(state[name])
            }
        return commons


    def get_buses(self) -> dict:
        buses = {}
        root = self.BUSES_ROOT
        state = self.json

        for bus in state[root]:
            buses[bus] = self.get_element_properties(state[root][bus])
        return buses
    

    #it works due to inputs always sorted by input number
    def get_active_input(self, active_number: int=-1) -> dict:
        if active_number <= 0: return {}
        active_input = {}
        state = self.json
        inputs = state[self.INPUTS_ROOT]["input"]
        
        return self.get_element_properties(inputs[active_number - 1])


    #inputs which we need to mon, found by user defined keys
    def get_needed_inputs(self) -> dict:
        needed_inputs = {}
        state = self.json
        keys = self.keys

        inputs = state[self.INPUTS_ROOT]["input"]
        for input in inputs:
            input_title = input["@title"]
            input_number = input["@number"]

            if any(el in input_title for el in keys):
                needed_inputs[input_number] = self.get_element_properties(input)

        return needed_inputs


    #inputs info got same way as get_active_input
    def get_used_overlays(self) -> dict:
        used_overlays = {}
        state = self.json

        inputs = state[self.INPUTS_ROOT]["input"]
        for overlay in state[self.OVERLAYS_ROOT]["overlay"]:
            if not "#text" in overlay: continue
            used_overlays[overlay["@number"]] = inputs[int(overlay["#text"]) - 1]
            if int(overlay["#text"]) == self.LAST_OVERLAY_NUMBER: break 
        return used_overlays