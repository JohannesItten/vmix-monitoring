import pprint
import time
import VmixXMLParser as Parser
import StateRule


class VmixState:
    def __init__(self, xml_snapshot, rule: StateRule):
        self.xml_snapshot = xml_snapshot
        self.rule = rule
        self.snapshot = None
        self.errors = []
        self.last_update = int(time.time())

    def update_state(self):
        parser = Parser.VmixXMLParser(self.xml_snapshot, self.rule.inputs_keys)
        self.snapshot = parser.parse()
        state_always = self.__check_state(self.rule.always)
        is_online = self.__is_online()
        check_rules = self.rule.online if is_online else self.rule.offline
        state_at_work = self.__check_state(check_rules)
        print(f'\nIs Online: {is_online}\n')
        print('At Work')
        pprint.pp(state_at_work)
        print('Always')
        pprint.pp(state_always)

    def __check_state(self, rules):
        errors = []
        for rule in rules:
            if rule is None:
                continue
            function_name = rule['function']
            function_args = rule['args']
            error_verbosity = rule['verbosity']
            function = getattr(self, function_name)
            function_result = function(*function_args)
            if not function_result and not rule['invert_result']:
                errors.append(f'{function_name} {function_result}')
        return errors

    def __is_online(self):
        active_title = self.snapshot.active_input.title
        idle_keys = self.rule.idle_keys
        return not any(s in active_title for s in idle_keys)

    # check that we have all user keys in preset
    def is_preset_ok(self):
        found_keys = list(self.snapshot.inputs.keys())
        found_keys.sort()
        self.rule.inputs_keys.sort()
        return found_keys == self.rule.inputs_keys

    def is_streaming(self):
        return self.snapshot.vmix_global.get_value('streaming')

    def is_recording(self):
        return self.snapshot.vmix_global.get_value('recording')

    def is_external(self):
        return self.snapshot.vmix_global.get_value('external')

    def is_bus_muted(self, bus_short_name):
        if bus_short_name not in self.snapshot.buses:
            return True
        bus = self.snapshot.buses[bus_short_name]
        return bus.volume_bar == 0 or bus.is_muted

    def is_input_bus_mapping_correct(self, input_key, needed_bus_mapping):
        if input_key not in self.snapshot.inputs.keys():
            return False
        input = self.snapshot.inputs[input_key][0]
        input_buses = input.get_prop('audiobusses')
        if input_buses is None:
            return False
        needed_bus_mapping = ','.join(needed_bus_mapping)
        return input_buses == needed_bus_mapping

    def __cut_delta(self):
        pass
