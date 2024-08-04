from common.rule.CheckRule import CheckRule


class CheckRulesStorage:
    def __init__(self,
                 name: str,
                 idle_keys: dict,
                 inputs_keys: dict,
                 buses: dict,
                 online: list,
                 offline: list,
                 always: list):
        self.name = name
        self.idle_keys = idle_keys
        self.inputs_keys = inputs_keys
        self.buses = buses
        self.online = online
        self.offline = offline
        self.always = always
