import xmltodict
import VmixInput as VmixInput
import VmixBus as VmixBus
import VmixGlobal as VmixGlobal

from lxml import etree
import pprint

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

    BUSES_ROOT_TAG = 'audio'
    INPUTS_ROOT_TAG = 'inputs'
    OVERLAYS_ROOT_TAG = 'overlays'

    INPUT_OVERLAY_TAG = 'overlay'
    INPUT_TEXT_TAG = 'text'

    LAST_OVERLAY_NUMBER = 4 #cause overlays 5-8 - stingers


    def __init__(self, xml, input_keys=[]):
        self.input_keys = input_keys
        self.xml_root = etree.fromstring(xml)


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


    # Skip things like dynamic and transitions
    # This is done in order not to store unnecessary information. 
    # It is better to parse nested structures separately 
    # and extract from them only the information 
    # necessary for monitoring
    def get_global_elements(self) -> VmixGlobal:
        root = self.xml_root
        globals = {}
        for element in root.getchildren():
            if len(element.getchildren()) > 0:
                continue
            globals[element.tag] = {
                "value": element.text,
                "props": self.get_element_attributes(element)
            }
        return VmixGlobal.VmixGlobal(globals)


    #store attributes like meterF1, meterF2:
    #{meterF:
    # {'1': '0.98'}
    # {'2': '0.97'}
    #}
    #all other as key=val
    def get_element_attributes(self, element):
        attributes = {}
        for key, value in element.items():
            if key[-1].isalpha():
                attributes[key] = value
                continue
            attribute_name = key[:-1]
            attribute_number = key[-1]
            if attribute_name not in attributes:
                attributes[attribute_name] = {}
            attributes[attribute_name] = {attribute_number: value}

        return attributes


    def __get_nested_root(self, tag):
        nested_iter = self.xml_root.iter(tag)
        nested_root = next(nested_iter, None)
        return nested_root


    #list of keys/guid's of input multiview overlays
    def get_input_overlays(self, input) -> list:
        input_overlays = []
        for element in input.findall(self.INPUT_OVERLAY_TAG):
            input_overlays.append(element.get('key'))
        return input_overlays


    #text fields of input type=GT
    #{'name': 'text value'}
    def get_input_texts(self, input) -> dict:
        input_texts = {}
        for element in input.findall(self.INPUT_TEXT_TAG):
            text_name = element.get('name')
            input_texts[text_name] = element.text
        return input_texts


    def get_buses(self) -> list:
        buses = []
        bus_root = self.__get_nested_root(self.BUSES_ROOT_TAG)
        if bus_root is None: return []

        for bus in bus_root.getchildren():
            bus_props = self.get_element_attributes(bus)
            buses.append(VmixBus.VmixBus(
                name=bus.tag,
                is_muted=eval(bus_props['muted']),
                volume_bar=float(bus_props['volume']),
                props=bus_props
            ))
        return buses
    

    #it works due to inputs always sorted by input number
    def get_input(self, input_number: int=-1) -> VmixInput:
        input_number = input_number - 1
        inputs = self.__get_nested_root(self.INPUTS_ROOT_TAG)
        try:
            input = inputs[input_number]
        except IndexError:
            return None

        input_attributes = self.get_element_attributes(input)
        input_obj = VmixInput.VmixInput(
            number=input_attributes['number'],
            key=input_attributes['key'],
            title=input_attributes['title'],
            overlays=self.get_input_overlays(input),
            texts=self.get_input_texts(input),
            props=input_attributes
        )
        return input_obj


    #inputs which we need to mon, found by user defined keys
    def get_needed_inputs(self) -> list:
        needed_inputs = []
        input_root = self.__get_nested_root(self.INPUTS_ROOT_TAG)
        if input_root is None: return []

        for input in input_root.getchildren():
            input_attributes = self.get_element_attributes(input)
            input_title = input_attributes['title']
            input_number = int(input_attributes['number'])

            if any(el in input_title for el in self.input_keys):
                input_obj = VmixInput.VmixInput(
                    number=input_number,
                    key=input_attributes['key'],
                    title=input_title,
                    overlays=self.get_input_overlays(input),
                    texts=self.get_input_texts(input),
                    props=input_attributes
                )
                needed_inputs.append(input_obj)
        return needed_inputs


    #inputs info got same way as get_active_input
    def get_used_overlays(self) -> dict:
        overlays_root = self.__get_nested_root(self.OVERLAYS_ROOT_TAG)
        if overlays_root is None: return {}
        used_overlays = {}

        for overlay in overlays_root:
            if overlay.text is None: continue
            overlay_number = overlay.get('number')
            input_number = int(overlay.text)
            used_overlays[overlay_number] = self.get_input(input_number)
            if int(overlay_number) == self.LAST_OVERLAY_NUMBER: break 
        return used_overlays