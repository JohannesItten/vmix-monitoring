from lxml import etree
import VmixBus
import VmixGlobal
import VmixInput
import VmixSnapshot


def get_element_attributes(element):
    attributes = {}
    for key, value in element.items():
        if key[-1].isalpha():
            attributes[key] = value
            continue
        attribute_name = key[:-1]
        attribute_number = key[-1]
        if attribute_name not in attributes:
            attributes[attribute_name] = {}
        attributes[attribute_name][attribute_number] = value

    return attributes


class VmixXMLParser:
    BUSES_ROOT_TAG = 'audio'
    INPUTS_ROOT_TAG = 'inputs'
    OVERLAYS_ROOT_TAG = 'overlays'

    MIX_TAG = 'mix'
    ACTIVE_TAG = 'active'

    INPUT_OVERLAY_TAG = 'overlay'
    INPUT_TEXT_TAG = 'text'

    LAST_OVERLAY_NUMBER = 4  # cause overlays 5-8 - stingers

    def __init__(self, xml, input_keys=None):
        if input_keys is None:
            input_keys = []
        self.input_keys = input_keys
        self.xml_root = etree.fromstring(xml)

    def parse(self) -> VmixSnapshot:
        vmix_global = self.__get_global_elements()
        active_input_number = vmix_global.get_value('active')
        active_input = self.__get_input(active_input_number)

        return VmixSnapshot.VmixSnapshot(
            vmix_global=vmix_global,
            active_input=active_input,
            buses=self.__get_buses(),
            inputs=self.__get_needed_inputs(),
            overlays=self.__get_used_overlays(),
            mixes=self.__get_mix_active_input()
        )

    # Skip things like dynamic and transitions
    # This is done in order not to store unnecessary information. 
    # It is better to parse nested structures separately 
    # and extract from them only the information 
    # necessary for monitoring
    def __get_global_elements(self) -> VmixGlobal:
        root = self.xml_root
        globals = {}
        for element in root.getchildren():
            if len(element.getchildren()) > 0:
                continue
            globals[element.tag] = {
                'value': element.text,
                'props': get_element_attributes(element)
            }
        return VmixGlobal.VmixGlobal(globals)

    # store attributes like meterF1, meterF2:
    # {meterF:
    # {'1': '0.98'}
    # {'2': '0.97'}
    # }
    # all other as key=val

    def __get_nested_root(self, tag):
        nested_iter = self.xml_root.iter(tag)
        nested_root = next(nested_iter, None)
        return nested_root

    # list of keys/guid's of input multiview overlays
    def __get_input_overlays(self, input) -> list:
        input_overlays = []
        for element in input.findall(self.INPUT_OVERLAY_TAG):
            input_overlays.append(element.get('key'))
        return input_overlays

    # text fields of input type=GT
    # {'name': 'text value'}
    def __get_input_texts(self, input) -> dict:
        input_texts = {}
        for element in input.findall(self.INPUT_TEXT_TAG):
            text_name = element.get('name')
            input_texts[text_name] = element.text
        return input_texts

    def __get_buses(self) -> dict:
        buses = {}
        bus_root = self.__get_nested_root(self.BUSES_ROOT_TAG)
        if bus_root is None:
            return {}

        for bus in bus_root.getchildren():
            bus_props = get_element_attributes(bus)
            bus_obj = VmixBus.VmixBus(
                name=bus.tag,
                is_muted=eval(bus_props['muted']),
                volume_bar=float(bus_props['volume']),
                props=bus_props
            )
            buses[bus_obj.short_name] = bus_obj
        return buses

    # it works due to inputs always sorted by input number
    def __get_input(self, input_number: int = -1) -> VmixInput:
        input_number = input_number - 1
        inputs = self.__get_nested_root(self.INPUTS_ROOT_TAG)
        try:
            input = inputs[input_number]
        except IndexError:
            return None

        input_attributes = get_element_attributes(input)
        input_obj = VmixInput.VmixInput(
            number=input_attributes['number'],
            key=input_attributes['key'],
            title=input_attributes['title'],
            vmix_type=input_attributes['type'],
            overlays=self.__get_input_overlays(input),
            texts=self.__get_input_texts(input),
            props=input_attributes
        )
        return input_obj

    # inputs which we need to mon, found by user defined keys
    def __get_needed_inputs(self) -> dict:
        needed_inputs = {}
        input_root = self.__get_nested_root(self.INPUTS_ROOT_TAG)
        if input_root is None:
            return {}

        for input in input_root.getchildren():
            input_attributes = get_element_attributes(input)
            input_title = input_attributes['title']
            input_number = int(input_attributes['number'])

            for key in self.input_keys:
                if key not in input_title:
                    continue
                input_obj = VmixInput.VmixInput(
                    number=input_number,
                    key=input_attributes['key'],
                    title=input_title,
                    vmix_type=input_attributes['type'],
                    overlays=self.__get_input_overlays(input),
                    texts=self.__get_input_texts(input),
                    props=input_attributes,
                    user_key=key
                )
                needed_inputs[key] = input_obj
        return needed_inputs

    # inputs info got same way as get_active_input
    def __get_used_overlays(self) -> dict:
        overlays_root = self.__get_nested_root(self.OVERLAYS_ROOT_TAG)
        if overlays_root is None:
            return {}
        used_overlays = {}

        for overlay in overlays_root:
            if overlay.text is None:
                continue
            overlay_number = overlay.get('number')
            input_number = int(overlay.text)
            used_overlays[overlay_number] = self.__get_input(input_number)
            if int(overlay_number) == self.LAST_OVERLAY_NUMBER:
                break
        return used_overlays

    # mix 2+ active inputs
    def __get_mix_active_input(self) -> dict:
        active_inputs = {}
        mixes = self.xml_root.findall(self.MIX_TAG)

        for mix in mixes:
            active = mix.find(self.ACTIVE_TAG)
            mix_number = mix.get('number')
            input_number = int(active.text)
            if input_number == 0:
                active_inputs[mix_number] = None
                continue
            active_inputs[mix_number] = self.__get_input(input_number)
        return active_inputs
