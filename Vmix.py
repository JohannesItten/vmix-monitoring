import hashlib
import VmixXMLParser as Parser
import VmixState as VmixState

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
        parser = Parser.VmixXMLParser(xml=xml_state, 
                                    keys=["zastkey", "testkey", "audiokey"])

        snapshot = parser.parse()

        input_to_check = {}
        current_state = VmixState.VmixState(snapshot, {})
        for number in snapshot["needed"]:
            input = snapshot["needed"][number]
            if 'audiokey' in input['title']:
                input_to_check = input
        print("BusMap:", current_state.is_input_bus_mapping(input_to_check))
        print("isMuted:", current_state.is_input_muted(input_to_check))                                    
        # if current_state != self.state:
        #     self.is_changed = True
        #     self.level = Vmix.INFO
        #     self.state = current_state
        # else:
        #     self.is_changed = False


    #old functionality
    def is_on_air(self) -> bool:
        return self.state["online"]
