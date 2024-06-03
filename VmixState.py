import hashlib
from pickle import NONE
import xmltodict


class VmixState:

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
        self.level = VmixState.INFO
        self.is_changed = False


    def __str__(self):
        return "{} : {}".format(self.id, self.ip)


    def __eq__(self, other) -> bool:
        return self.state == other.state and self.ip == other.ip


    def updateState(self, xml_state):
        json_state = xmltodict.parse(xml_state)['vmix']
        current_state = {
                "version": json_state['version'],
                "online": False,
                "recording": False,
                "streaming": False,
                "streaming_channels": [],
                "speaker": None,
                "timer": None,
                "master": {"state": False, "volume": 0},
                "busA": {"state": False, "volume": 0},
                "busB": {"state": False, "volume": 0},  
                "parse_error": {
                                "zast": True,
                                "speaker": True,
                                "timer": True,
                                } #error means there vmix preset parse errors  
            }
        # find input nums with zast_key in title
        # find key's of title inputs
        pgm_input = None
        pgm_input_num = json_state["active"]
        zast_key = "zastkey"
        zast_input_nums = []
        speaker_key = "speakerkey"
        speaker_inputs = {}
        timer_key = "timerkey"
        timer_inputs = []
        
        for input in json_state["inputs"]["input"]:
            input_title = input["@title"]
            input_num = input["@number"]
            
            if input_num == pgm_input_num:
                pgm_input = input

            if input_title.find(zast_key) >= 0:
                zast_input_nums.append(input_num)
            elif input_title.find(speaker_key) >= 0:
                speaker_inputs[input["@key"]] = input
            elif input_title.find(timer_key) >= 0:
                timer_inputs.append(input)

        #check that every needed input is found
        current_state["parse_error"] = {
                "zast": len(zast_input_nums) > 0,
                "speaker": len(speaker_inputs) > 0,
                "timer": len(timer_inputs)
                }

        #check is input with zast_key in pgm
        if pgm_input_num not in zast_input_nums:
            current_state["online"] = True
        
        #get inputs in overlays
        overlay_inputs = []
        for overlay in json_state["overlays"]["overlay"]:
            if "#text" in overlay:
                overlay_inputs.append(overlay["#text"])
        
        #get speaker name from title input
        #check name in overlay
        overlay_name = ""
        for guid, input in speaker_inputs.items():
            if input["@number"] in overlay_inputs:
                overlay_name = self.get_name_from_overlay(input)
        current_state["speaker"] = overlay_name
        #
        
        #check timer state
        if (len(timer_inputs) > 0):
            current_state["speaker"] += " " + self.get_timer_state(timer_inputs[0])

        #check is recording
        if "#text" in json_state["recording"]:
            current_state["recording"] = eval(json_state["recording"]["#text"])
        else:
            current_state["recording"] = eval(json_state["recording"])
            
        #check is streaming
        if "#text" in json_state["streaming"]:
            current_state["streaming"] = eval(json_state["streaming"]["#text"])
            streaming = json_state["streaming"]
            current_state["streaming_channels"] = [key[-1:] for key in streaming if key in ["@channel1", "@channel2", "@channel3"]]
        else:
            current_state["streaming"] = eval(json_state["streaming"])
        
        #audio buses
        for bus_name in json_state["audio"]:
            if bus_name in ["master", "busA", "busB"]:
                bus_state = json_state["audio"][bus_name]
                state = not eval(bus_state["@muted"])
                volume = round(float(bus_state["@volume"]))
                if volume < 30:
                    state = False
                current_state[bus_name] = {
                        "state": state, 
                        "volume": volume,
                        }
                                            
        if current_state != self.state:
            self.is_changed = True
            self.level = VmixState.INFO
            self.state = current_state
        else:
            self.is_changed = False


    def get_timer_state(self, input) -> str:
        if "text" not in input and len(input["text"]) < 1:
            return ""
        
        timer = ""
        try:
            timer = input["text"]["#text"]
        except:
            print("Can't parse timer")

        return timer
        
    
    def get_name_from_overlay(self, input) -> str:
        if "text" not in input and len(input["text"]) < 1:
            return ""
        
        name = ""
        try:
            fullname = input["text"][0]["#text"]
            surname = fullname.split(" ")[0]
            name = surname
        except:
            print("Can't parse name")

        return name
    
    
    def get_name_from_input(self, input, speaker_inputs) -> str:
        fullname = ""
        speaker = None
        for layer in input["overlay"]:
            if layer["@key"] not in speaker_inputs.keys():
                continue
            speaker = speaker_inputs[layer["@key"]]
            break
        
        if not speaker: return fullname
        
        lastname = speaker["text"][2]["#text"]
        src_name = speaker["text"][1]["#text"].split(" ")
        name = ""
        for n in src_name:
            name += n[:1] + "."
        fullname = lastname + " " + name

        return fullname
    

    def is_on_air(self) -> bool:
        return self.state["online"]
