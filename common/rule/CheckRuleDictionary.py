INVERT_RESULT_KEY = '/'

# user_function_name (rules.yaml): {
#    real_function_name,
#    error if function return False,
#    error if function return True. It needs for inverted results
# }

RULES_DICTIONARY = {
    'streaming': {
        'func': 'is_streaming',
        'onTrue': 'The Streaming button is NOT pressed',
        'onFalse': 'The Streaming button is pressed'
    },
    'recording': {
        'func': 'is_recording',
        'onTrue': 'The Recording button is NOT pressed',
        'onFalse': 'The Recording button is pressed'
    },
    'external': {
        'func': 'is_external',
        'onTrue': 'The External button is NOT pressed',
        'onFalse': 'The External button is pressed'
    },
    'busMuted': {
        'func': 'is_bus_muted',
        'onTrue': 'The bus is NOT muted',
        'onFalse': 'The bus is muted'
    },
    'inputMuted': {
        'func': 'is_input_muted',
        'onTrue': 'The input is NOT muted',
        'onFalse': 'The input is muted'
    },
    'inputBus': {
        'func': 'is_input_bus_mapping_correct',
        'onTrue': 'Required buses is not enabled',
        'onFalse': 'All required buses enabled'
    },
    'multiCorder': {
        'func': 'is_multicorder',
        'onTrue': 'The MultiCorder button is NOT pressed',
        'onFalse': 'The MultiCorder button is pressed'
    },
    'fullscreen': {
        'func': 'is_fullscreen',
        'onTrue': 'The Fullscreen button is NOT pressed',
        'onFalse': 'The Fullscreen button is pressed'
    },
    'cutFrequencyOk': {
        'func': 'is_cut_frequency_ok',
        'onTrue': 'The director fell asleep',
        'onFalse': 'The director is working as he should'
    },
    'busLevelLow': {
        'func': 'is_bus_level_low',
        'onTrue': 'The bus level is NOT low',
        'onFalse': 'The bus level is low',
    },
    'inputLevelLow': {
        'func': 'is_input_level_low',
        'onTrue': 'The input level is NOT low',
        'onFalse': 'The input level is low'
    }
}
