INVERT_RESULT_KEY = '/'

# user_function_name (rules.yaml): [
#    real_function_name,
#    error if function return False,
#    error if function return True. It need's for inverted results
# ]

RULES_DICTIONARY = {
    'streaming': [
        'is_streaming',
        'The Streaming button is NOT pressed',
        'The Streaming button is pressed'
    ],
    'recording': [
        'is_recording',
        'The Recording button is NOT pressed',
        'The Recording button is pressed'
    ],
    'external': [
        'is_external',
        'The External button is NOT pressed',
        'The External button is pressed'
    ],
    'preset': [
        'is_preset_ok',
        'The vMix preset does not contain the required keys',
        'The preset contains all the necessary keys'
    ],
    'busMuted': [
        'is_bus_muted',
        'The bus is NOT muted',
        'The bus is muted'
    ],
    'inputMuted': [
        'is_input_muted',
        'The input is NOT muted',
        'The input is muted'
    ],
    'inputBus': [
        'is_input_bus_mapping_correct',
        'Required buses is not enabled',
        'All required buses enabled'
    ],
    'multiCorder': [
        'is_multicorder',
        'The MultiCorder button is NOT pressed',
        'The MultiCorder button is pressed'
    ],
    'fullscreen': [
        'is_fullscreen',
        'The Fullscreen button is NOT pressed',
        'The Fullscreen button is pressed'
    ]
}
