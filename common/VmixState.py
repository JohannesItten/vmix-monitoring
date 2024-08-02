import time
from common import StateRule, VmixXMLParser as Parser


class VmixState:
    def __init__(self, xml_snapshot, rule: StateRule):
        self.xml_snapshot = xml_snapshot
        self.rule = rule
        self.snapshot = None
        self.errors = {
            'parsing': [],
            'error': [],
            'warning': [],
            'info': []
        }
        self.last_update = int(time.time())
        self.snapshot_dump = None
        self.online = None

    def update_state(self):
        parser = Parser.VmixXMLParser(self.xml_snapshot, self.rule.inputs_keys)
        self.snapshot = parser.parse()
        self.__check_state(self.rule.always)
        self.online = self.__is_online()
        check_rules = self.rule.online if self.online else self.rule.offline
        self.__check_state(check_rules)
        self.snapshot_dump = self.snapshot.dump()

    def __check_state(self, rules):
        is_preset = self.is_preset_ok()
        if not is_preset['result']:
            error_text = 'The vMix preset does not contain the required keys'
            self.errors['parsing'].append(
                '{} ({})'.format(error_text, is_preset['info'])
            )
            return
        for rule in rules:
            if rule is None:
                continue
            function = getattr(self, rule['function'])
            function_result = function(*rule['args'])
            function_result_value = function_result['result']
            function_result_info = function_result['info']
            if function_result_value is None:
                self.errors['parsing'].append(function_result_info)
                continue
            if function_result_value == rule['expected_result']:
                continue
            error_verbosity = rule['error_verbosity']
            if error_verbosity not in self.errors:
                continue
            error_description = rule['error_description']
            if function_result_info is not None:
                error_description = error_description + f' ({function_result_info})'
            self.errors[error_verbosity].append(error_description)

    def __is_online(self):
        if self.snapshot.active_input is None:
            return False
        active_title = self.snapshot.active_input.title
        idle_keys = self.rule.idle_keys
        return not any(s in active_title for s in idle_keys)

    # check that we have all user keys in preset
    def is_preset_ok(self):
        found_keys = list(self.snapshot.inputs.keys())
        found_keys.sort()
        needed_keys = self.rule.inputs_keys
        needed_keys.sort()
        result = found_keys == needed_keys
        info = ','.join([x for x in needed_keys if x not in found_keys])
        return {
            'result': result,
            'info': info
        }

    def is_streaming(self):
        result = self.snapshot.vmix_global.get_value('streaming')
        return {
            'result': result,
            'info': None
        }

    def is_recording(self):
        result = self.snapshot.vmix_global.get_value('recording')
        return {
            'result': result,
            'info': None
        }

    def is_external(self):
        result = self.snapshot.vmix_global.get_value('external')
        return {
            'result': result,
            'info': None
        }

    def is_multicorder(self):
        result = self.snapshot.vmix_global.get_value('multiCorder')
        return {
            'result': result,
            'info': None
        }

    def is_fullscreen(self):
        result = self.snapshot.vmix_global.get_value('fullscreen')
        return {
            'result': result,
            'info': None
        }

    def is_bus_muted(self, bus_short_name):
        if bus_short_name not in self.snapshot.buses:
            return {
                'result': None,
                'info': f'Bus not found in preset ({bus_short_name})'
            }
        bus = self.snapshot.buses[bus_short_name]
        result = bus.volume_bar == 0 or bus.is_muted
        return {
            'result': result,
            'info': bus_short_name
        }

    def is_input_muted(self, input_key):
        if input_key not in self.snapshot.inputs.keys():
            return {
                'result': None,
                'info': f'Input not found in preset ({input_key})'
            }
        vmix_input = self.snapshot.inputs[input_key]
        try:
            is_muted = eval(vmix_input.get_prop('muted'))
            volume_bar = float(vmix_input.get_prop('volume'))
        except (TypeError, ValueError) as e:
            return {
                'result': None,
                'info': f'Input has no sound enabled ({input_key})'
            }
        result = is_muted or volume_bar == 0
        return {
            'result': result,
            'info': input_key
        }

    def is_input_bus_mapping_correct(self, input_key, needed_bus_mapping):
        if input_key not in self.snapshot.inputs.keys():
            return {
                'result': None,
                'info': f'Input not found in preset ({input_key})'
            }
        vmix_input = self.snapshot.inputs[input_key]
        input_buses = vmix_input.get_prop('audiobusses')
        if input_buses is None:
            return {
                'result': None,
                'info': f'Input has no sound enabled ({input_key})'
            }
        needed_bus_mapping = ','.join(needed_bus_mapping)
        result = input_buses == needed_bus_mapping
        info = '{}: {} required: ({})'.format(
            input_key,
            ','.join(input_buses),
            needed_bus_mapping
        )
        return {
            'result': result,
            'info': info
        }

    def __cut_delta(self):
        pass

    def __bus_level_low(self):
        pass

    def __input_level_low(self):
        pass
