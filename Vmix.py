import hashlib
import VmixXMLParser as Parser
import VmixState as VmixState
import VmixInput as VmixInput
import VmixGlobal as VmixGlobal

import pprint




class Vmix:

    INFO = 0
    NOTICE = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, ip, studio_name, skip = False):
        self.id = hashlib.md5((studio_name + ip).encode("utf-8")).hexdigest()
        self.ip = ip
        self.studio_name = studio_name
        self.skip = skip
        self.state = {}
        self.level = Vmix.INFO
        self.is_changed = False


    def __str__(self):
        return "{} : {}".format(self.id, self.ip)


    def __eq__(self, other) -> bool:
        return self.state == other.state and self.ip == other.ip


    def updateState(self, xml_state):
        input_keys = ["zastkey", "testkey", "audiokey", "multikey", "titlekey"]
        parser = Parser.VmixXMLParser(xml=xml_state, input_keys=input_keys)

        snapshot = parser.parse()
        GLOBALS = [
            'version',
            'edition',
            'streaming',
            'recording',
            'external',
            'playList',
            'multiCorder',
            'fullscreen',
            'preview',
            'active',
            'preset'
            ]

        print('===BUSES===')
        for b in snapshot['buses']:
            print(f'Bus {b.short_name}: {b.dbfs}, {b.volume}')

        print('\n===INPUTS===')
        for i in snapshot['needed']:
            print(i)

        print('\n===VMIX GLOBAL===')
        for i in GLOBALS:
            print(f'{i}: {snapshot['global'].get_value(i)}')

        print('\n===ACTIVE===')
        print(snapshot['active'])

        print('\n===ACTIVE OVERLAYS===')
        for key, val in snapshot['overlays'].items():
            print(f'{key}: {val}')

        # print(snapshot["global"])

        # current_state = VmixState.VmixState(snapshot, {})
        # for input in snapshot["needed"]:
        #     if 'audiokey' in input.title:
        #         bus_map_res = current_state.is_input_bus_mapping(input)
        #         is_muted_res = current_state.is_input_muted(input)
        # print("BusMap(MABC):", bus_map_res)
        # print("IsMuted:", is_muted_res)

        # print("BusMap:", current_state.is_input_bus_mapping(input_to_check))
        # print("isMuted:", current_state.is_input_muted(input_to_check))  


    #old functionality
    def is_on_air(self) -> bool:
        return self.state["online"]
