class CheckRule(object):
    def __init__(self, function, args, expected_result, error_verbosity, error_description):
        self.function = function
        self.args = args
        self.expected_result = expected_result
        self.error_verbosity = error_verbosity
        self.error_description = error_description
        self.id = self.__get_id()

    def is_correct(self):
        return True

    def __get_id(self):
        args_str = ''
        for arg in self.args:
            args_str += str(arg)
        return (self.function +
                args_str +
                str(self.expected_result))
