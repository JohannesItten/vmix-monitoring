import hashlib
from pickle import NONE
import xmltodict


class VmixState:

    INFO = 0
    NOTICE = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, ip, studio_name):
        self.id = hashlib.md5((studio_name + ip).encode("utf-8")).hexdigest()
        self.ip = ip
        self.studio_name = studio_name
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
                "master": {"state": False, "volume": 0},
                "busA": {"state": False, "volume": 0}, 
                "audio": {"muted": True, "volume": 0},
                "audio_zoom": {"muted": True, "volume": 0},
                "parse_error": {
                                "zast": True,
                                "audio": True,
                                "zoom": True,
                                "speaker": True
                                } #error means there vmix preset parse errors  
            }
        # find input nums with zast_key in title
        # find key's of title inputs
        pgm_input = None
        pgm_input_num = json_state["active"]
        zast_key = "zastkey"
        speaker_key = "speakerkey"
        speaker_inputs = []
        zast_input_nums = []

        audio_in_key = "audiokey"
        audio_inputs = []

        zoom_in_key = "zoomkey"
        zoom_inputs = []
        
        for input in json_state["inputs"]["input"]:
            input_title = input["@title"]
            input_num = input["@number"]
            
            if input_num == pgm_input_num:
                pgm_input = input

            if input_title.find(zast_key) >= 0:
                zast_input_nums.append(input_num)
            elif input_title.find(speaker_key) >= 0:
                speaker_inputs.append(input)
            elif input_title.find(audio_in_key) >= 0:
                audio_inputs.append(input)
            elif input_title.find(zoom_in_key) >= 0:
                zoom_inputs.append(input)

        #check that every needed input is found
        current_state["parse_error"] = {
                "zast": len(zast_input_nums) > 0,
                "audio": len(audio_inputs) > 0,
                "audio_zoom": len(zoom_inputs) > 0,
                "speaker": len(speaker_inputs) > 0
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
        for input in speaker_inputs:
            if input["@number"] in overlay_inputs:
                current_state["speaker"] = self.get_name_from_input(input)

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
        
        #audio inputs
        for input in audio_inputs:
            if "@muted" not in input:
                current_state["audio"] = {
                        "state": False,
                        "volume": "off"
                        }
                break
            state = not eval(input["@muted"])
            volume = round(float(input["@volume"]))
            if volume < 40:
                state = False
            current_state["audio"] = {
                    "state": state,
                    "volume": volume
                    }

        #zoom inputs
        for input in zoom_inputs:
            if "@muted" not in input:
                current_state["audio_zoom"] = {
                        "state": False,
                        "volume": "off"
                        }
                break
            state = not eval(input["@muted"])
            volume = round(float(input["@volume"]))
            if volume < 40:
                state = False
            current_state["audio_zoom"] = {
                    "state": state,
                    "volume": volume
                    }


        #audio buses
        for bus_name in json_state["audio"]:
            if bus_name in ["master", "busA"]:
                bus_state = json_state["audio"][bus_name]
                state = not eval(bus_state["@muted"])
                volume = round(float(bus_state["@volume"]))
                if volume < 40:
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


    def get_name_from_input(self, input) -> str:
        if "text" not in input and len(input["text"]) < 1:
            return ""

        fullname = input["text"][1]["#text"]
        return fullname.split(" ")[0]
