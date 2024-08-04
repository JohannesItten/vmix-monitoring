import yaml
from common import Vmix
from common.rule import CheckRulesStorage, CheckRule
from common.rule.CheckRuleDictionary import RULES_DICTIONARY, INVERT_RESULT_KEY


def translate_rules(rule_list) -> list:
    real_rules = []
    for user_rule in rule_list:
        func_name = user_rule[0]
        expected_result = True
        if INVERT_RESULT_KEY in func_name:
            func_name = func_name[1:]
            expected_result = False
        if func_name not in RULES_DICTIONARY:
            continue
        translated_rule = RULES_DICTIONARY[func_name]
        if expected_result:
            error_description = translated_rule['onTrue']
        else:
            error_description = translated_rule['onFalse']
        real_rule = CheckRule.CheckRule(
            function=translated_rule['func'],
            args=user_rule[1],
            expected_result=expected_result,
            error_verbosity=user_rule[2],
            error_description=error_description
        )
        real_rules.append(real_rule)
    return real_rules


class ConfigReader:
    CONFIG_DIR = 'config/'

    def __init__(self):
        pass

    # TODO: user input check
    def read_rules(self, filename):
        rules = {}
        with open(file=self.CONFIG_DIR + filename, mode='r') as config:
            config_content = yaml.safe_load(config)
        for name, rule in config_content.items():
            state_rule = CheckRulesStorage.CheckRulesStorage(
                name=name,
                idle_keys=rule['idle'],
                inputs_keys=rule['watch'] + rule['idle'],
                buses=rule['buses'],
                online=translate_rules(rule['online']),
                offline=translate_rules(rule['offline']),
                always=translate_rules(rule['always'])
            )
            rules[name] = state_rule
        return rules

    def read_vmixes(self, filename):
        with open(file=self.CONFIG_DIR + filename, mode='r') as config:
            config_content = yaml.safe_load(config)
        vmixes = {}
        for key, vmix in config_content.items():
            if 'ip' not in vmix or 'name' not in vmix:
                continue
            vmix_obj = Vmix.Vmix(
                name=vmix['name'],
                unit=vmix['unit'],
                ip=vmix['ip'],
                port=vmix['port'],
                username=vmix['username'],
                password=vmix['password'],
                rule_name=vmix['rule']
            )
            vmixes[vmix_obj.id] = vmix_obj
        return vmixes

    def read_front(self, filename):
        with open(file=self.CONFIG_DIR + filename, mode='r') as config:
            config_content = yaml.safe_load(config)
        view_elements = {}
        default_icon = 'fa fa-cog'
        default_css_class = 'grey'
        for user_rule, user_elements in config_content.items():
            view_elements[user_rule] = {}
            for prop_name, prop in user_elements.items():
                if 'text' not in prop or 'icon' not in prop:
                    continue
                view_element = {
                    'text': prop['text'],
                    'icon': default_icon if prop['icon'] is None else prop['icon'],
                    'state': None,
                    'value': None,
                    'cssClass': default_css_class
                }
                view_elements[user_rule][prop_name] = view_element
        return view_elements

    def read_vmixes_ws(self, filename):
        with open(file=self.CONFIG_DIR + filename, mode='r') as config:
            config_content = yaml.safe_load(config)
        vmixes = []
        for key, vmix in config_content.items():
            if 'name' not in vmix:
                continue
            vmix_obj = Vmix.Vmix(
                name=vmix['name'],
                unit=vmix['unit'],
                ip=vmix['ip'],
                port=vmix['port'],
                username=vmix['username'],
                password=vmix['password'],
                rule_name=vmix['rule']
            )
            vmixes.append({
                'id': vmix_obj.id,
                'name': vmix['name'],
                'rule': vmix['rule']
            })
        return vmixes
