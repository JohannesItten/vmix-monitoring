import time


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
    def is_input_bus_mapping(self, input) -> bool:
        check_result = False
        buses_input_key = "audiobusses"
        bus_map = ["M", "A", "B"]
        if not buses_input_key in input: return False
        
        delimeter = ","
        bus_map_string = delimeter.join(bus_map)
        if bus_map_string == input[buses_input_key]: return True

        return check_result


    #TODO: add errors and desc

    
    def is_input_muted(self, input):
        check_result = True
        muted_key = "muted"
        volume_key = "volume"
        if not muted_key in input or not volume_key in input:
            return True
        if not eval(input[muted_key]) and float(input[volume_key]) != 0:
            return False
        return check_result


    def cut_delta(self):
        pass


    def check_bus_level(self):
        pass