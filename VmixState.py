import time
import VmixInput as VmixInput


class VmixState:
    #State consts
    STATE_NOT_CHECKED = -1
    STATE_OK = 0
    STATE_NOTICE = 1
    STATE_WARNING = 2
    STATE_ERROR = 3

    state = STATE_NOT_CHECKED
    description = ""
    errors = {} #{{"level": int, "desc": string}}
    last_update_time = int(time.time())


    def __init__(self, snapshot: dict, rules: dict):
        self.rules = rules
        self.snapshot = snapshot

    
    def updateState(self):
        pass

    
    def isStreaming(self):
        pass


    def isRecording(self):
        pass


    def is_on_air(self):
        pass
    

    def is_preset_ok(self):
        pass


    #TODO: add errors and desc
    def is_input_bus_mapping(self, input: VmixInput) -> bool:
        check_result = False
        buses_key = "audiobusses"
        bus_map = ["M", "A", "B"]
        prop_buses = input.get_prop(buses_key)
        if  prop_buses == -1: return False
        delimeter = ","
        bus_map_string = delimeter.join(bus_map)
        if bus_map_string == prop_buses: return True

        return check_result


    #TODO: add errors and desc
    def is_input_muted(self, input: VmixInput):
        check_result = True
        muted_key = "muted"
        volume_key = "volume"
        prop_muted = input.get_prop(muted_key)
        prop_volume = input.get_prop(volume_key)
        if prop_muted == -1 or prop_volume == -1:
            return True
        if not eval(prop_muted) and float(prop_volume) != 0:
            return False
        return check_result


    def cut_delta(self):
        pass


    def check_bus_level(self):
        pass