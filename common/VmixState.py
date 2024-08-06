import time
from common import VmixXMLParser as Parser
from common.rule import CheckRulesStorage
from common.check_result import TimeDepCheckResultStorage as ResultStorage
from common.check_error import CheckErrorStorage as ErrorStorage


class VmixState:
    def __init__(self, xml_snapshot, rules: CheckRulesStorage):
        self.xml_snapshot = xml_snapshot
        self.rules = rules
        self.snapshot = None
        self.errors = ErrorStorage.CheckErrorStorage()
        self.fixed_errors = []
        self.last_update = int(time.time())
        self.snapshot_dump = None
        self.online = None
        self.is_online_changed = False
        # stores check result updates and update times
        # need for checking value changes, during time
        self.check_results = ResultStorage.TimeDepCheckResultStorage()
        self.check_results.add_always_ids(self.rules.always)

    def update_state(self):
        self.__reinit_state()
        parser = Parser.VmixXMLParser(self.xml_snapshot, self.rules.inputs_keys)
        self.snapshot = parser.parse()
        self.__check_state(self.rules.always)
        current_online_state = self.__is_online()
        if (current_online_state != self.online and
                self.online is not None):
            self.is_online_changed = True
            # stop run time dependent checks on online state change
            self.check_results.reset_except_always()
        self.online = current_online_state
        check_rules = self.rules.online if self.online else self.rules.offline
        self.__check_state(check_rules)
        self.snapshot_dump = self.snapshot.dump()
        self.errors.sort()

    def __reinit_state(self):
        self.fixed_errors = []
        self.last_update = int(time.time())
        self.is_online_changed = False

    def __check_state(self, rules):
        is_preset = self.is_preset_ok()
        # All checks from user rules are not valid if preset check is failed
        if not is_preset['result']:
            error_text = 'The vMix preset does not contain the required keys'
            error_description = f'{error_text} ({is_preset["info"]})'
            self.errors.add_error('is_preset', error_description, 'parsing')
            return
        if 'is_preset' in self.errors.storage:
            self.fixed_errors.append(self.errors.remove_error('is_preset'))
        for rule in rules:
            if rule is None:
                continue
            function = getattr(self, rule.function)
            function_result = function(*rule.args)
            function_result_value = function_result['result']
            function_result_info = function_result['info']
            if function_result_value is None:
                self.errors.add_error(rule.id, function_result_info, 'parsing')
                continue
            if ('max_time' in function_result and
                    function_result['max_time'] > function_result['delta_time']):
                function_result_value = rule.expected_result
            if function_result_value == rule.expected_result:
                if rule.id in self.errors.storage.keys():
                    self.fixed_errors.append(self.errors.remove_error(rule.id))
                continue
            error_verbosity = rule.error_verbosity
            error_description = rule.error_description
            if function_result_info is not None:
                error_description = error_description + f' ({function_result_info})'
            self.errors.add_error(rule.id, error_description, error_verbosity)

    def __is_online(self):
        if self.snapshot.active_input is None:
            return False
        active_title = self.snapshot.active_input.title
        idle_keys = self.rules.idle_keys
        return not any(s in active_title for s in idle_keys)

    # check that we have all user keys in preset
    def is_preset_ok(self):
        found_keys = list(self.snapshot.inputs.keys())
        found_keys.sort()
        needed_keys = self.rules.inputs_keys
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
        except (TypeError, ValueError):
            return {
                'result': None,
                'info': f'Input has no sound at all({input_key})'
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
            input_buses,
            needed_bus_mapping
        )
        return {
            'result': result,
            'info': info
        }

    def is_cut_frequency_ok(self, max_delta_time):
        cut_delta_time = self.check_results.add_result(
            func='is_cut_frequency_ok',
            args=[max_delta_time],
            value=self.snapshot.active_input)
        return {
            'result': cut_delta_time < max_delta_time,
            'info': f'Last cut was {int(cut_delta_time)}s ago'
        }

    def is_bus_level_low(self, bus_short_name, low_level, low_max_time):
        if bus_short_name not in self.snapshot.buses.keys():
            return {
                'result': None,
                'info': f'Input not found in preset ({bus_short_name})'
            }
        bus = self.snapshot.buses[bus_short_name]
        is_level_low = False
        for dbfs in bus.dbfs:
            if dbfs >= low_level:
                continue
            is_level_low = True

        delta_time = self.check_results.add_result(
            func='is_bus_level_low',
            args=[bus_short_name, low_level, low_max_time],
            value=is_level_low
        )
        return {
            'result': is_level_low,
            'info': bus_short_name,
            'max_time': low_max_time,
            'delta_time': delta_time
        }

    def is_input_level_low(self, input_key, low_level, low_max_time):
        if input_key not in self.snapshot.inputs.keys():
            return {
                'result': None,
                'info': f'Input not found in preset ({input_key})'
            }
        vmix_input = self.snapshot.inputs[input_key]
        is_muted = vmix_input.get_prop('muted')
        if is_muted is None:
            return {
                'result': None,
                'info': f'Input has no sound at all ({input_key})'
            }

        is_muted = eval(is_muted)
        is_level_low = False
        for dbfs in vmix_input.dbfs:
            if dbfs >= low_level:
                continue
            is_level_low = True

        check_result = is_level_low or is_muted
        delta_time = self.check_results.add_result(
            func='is_input_level_low',
            args=[input_key, low_level, low_max_time],
            value=check_result
        )
        return {
            'result': check_result,
            'info': input_key,
            'max_time': low_max_time,
            'delta_time': delta_time
        }
