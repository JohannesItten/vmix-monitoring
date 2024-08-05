import common.check_result.TimeDepCheckResult as CheckResult


def get_result_id(func, args):
    result_id = func
    for arg in args:
        if arg is None:
            continue
        result_id += str(arg)
    return result_id


class TimeDepCheckResultStorage:
    def __init__(self):
        self.storage = {}
        # result_id's for funcs in user rules, tagged as always
        self.always_ids = []

    def add_result(self, func, args, value):
        result_id = get_result_id(func, args)
        if result_id in self.storage.keys():
            self.storage[result_id].update(value)
            return self.storage[result_id].delta_time
        self.storage[result_id] = CheckResult.TimeDepCheckResult(
            result_id=result_id,
            value=value
        )
        return 0

    def add_always_ids(self, user_rules):
        for check in user_rules:
            check_id = get_result_id(check['function'], check['args'])
            if check_id in self.always_ids:
                continue
            self.always_ids.append(check_id)

    def reset_except_always(self):
        for result_id in self.storage.keys():
            if result_id in self.always_ids:
                continue
            self.storage[result_id].reset_value()
