import hashlib
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
                "speaker": None
            }
        # check is input with zast_key in program
        # check current speaker in pgm
        pgm_input = json_state["active"]
        zast_key = "zastkey"
        speaker_key = "speakerkey"
        speaker_input_num = None
        speaker_name = None
        for input in json_state["inputs"]["input"]:
            input_title = input["@title"]
            if input_title.find("zastkey") >= 0:
                if input["@number"] != pgm_input:
                    current_state["online"] = True
            elif input_title.find("speakerkey") >= 0:
                speaker_input_num = input["@number"]
                speaker_name = input["text"][0]["#text"]
                if input["@number"] == pgm_input:
                    current_state["speaker"] = speaker_name
        
        #check speaker in overlay
        if speaker_input_num is not None:
            for overlay in json_state["overlays"]["overlay"]:
                if "#text" in overlay and overlay["#text"] == speaker_input_num:
                    current_state["speaker"] = speaker_name
        
        #check is streaming
        current_state["streaming"] = eval(json_state["streaming"])
        
        #check is rec
        if "#text" in json_state["recording"]:
            current_state["recording"] = eval(json_state["recording"]["#text"])
        else:
            current_state["recording"] = eval(json_state["recording"])
                    
        if current_state != self.state:
            self.is_changed = True
            self.level = VmixState.INFO
            self.state = current_state
        else:
            self.is_changed = False