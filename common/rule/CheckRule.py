class CheckRule(object):
    def __init__(self, function, args, expected_result, error_verbosity, error_description):
        self.function = function
        self.args = args
        self.expected_result = expected_result
        self.error_verbosity = error_verbosity
        self.error_description = error_description

    def is_correct(self):
        return True
