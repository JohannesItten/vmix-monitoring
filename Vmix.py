import hashlib
import VmixState as VmixState
import VmixInput as VmixInput
import VmixGlobal as VmixGlobal

import pprint

import config.ConfigReader as ConfigReader


class Vmix:
    INFO = 0
    NOTICE = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, ip, studio_name, skip=False):
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
        reader = ConfigReader.ConfigReader()
        rules = reader.read_rules('rules.yaml')
        # reader.read_vmixes('vmixes.yaml')
        state = VmixState.VmixState(xml_snapshot=xml_state, rule=rules['test'])
        state.update_state()
