INVERT_RESULT_KEY = '/'

RULE_GLOBAL = 'global'
RULE_BUS = 'bus'
RULE_INPUT = 'input'

# function/method name, params, type of check
# type of check needs to exclude multiple loops
RULES_DICTIONARY = {
    'streaming': ['is_streaming', RULE_GLOBAL],
    'recording': ['is_recording', RULE_GLOBAL],
    'external': ['is_external', RULE_GLOBAL],
    'presetOk': ['is_preset_ok', RULE_GLOBAL],
    'busMuted': ['is_bus_muted', RULE_BUS],
    'busMappingCorrect': ['is_input_bus_mapping_correct', RULE_INPUT]
}
