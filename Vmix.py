import hashlib
import VmixState as VmixState
import config.ConfigReader as ConfigReader


class Vmix:
    def __init__(self, ip, studio_name, skip=False):
        self.id = hashlib.md5((studio_name + ip).encode("utf-8")).hexdigest()
        self.ip = ip
        self.studio_name = studio_name
        self.skip = skip
        self.state = {}
        self.level = 0
        self.is_changed = False

    def __str__(self):
        return "{} : {}".format(self.id, self.ip)

    def __eq__(self, other) -> bool:
        return self.state == other.state and self.ip == other.ip

    def updateState(self, xml_state):
        reader = ConfigReader.ConfigReader()
        user_rules = reader.read_rules('rules.yaml')
        # reader.read_vmixes('vmixes.yaml')
        state = VmixState.VmixState(xml_snapshot=xml_state, rule=user_rules['test'])
        state.update_state()
