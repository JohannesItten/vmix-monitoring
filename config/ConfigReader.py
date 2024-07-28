import yaml
import StateRule
from UserRuleDictionary import RULES_DICTIONARY, INVERT_RESULT_KEY


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
        real_rule = RULES_DICTIONARY[func_name]
        real_rules.append({
            'function': real_rule[0],
            'args': user_rule[1],
            'expected_result': expected_result,
            'error_verbosity': user_rule[2],
            'error_description': real_rule[1] if expected_result else real_rule[2]
        })
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
            state_rule = StateRule.StateRule(
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
            rules = yaml.safe_load(config)
        # print(rules)
        pass
