from common.check_error import CheckError


class CheckErrorStorage:
    def __init__(self):
        self.storage = {}
        self.always_ids = []

    def add_error(self, rule_id: str, description: str, level):
        if rule_id in self.storage:
            self.storage[rule_id].description = description
        error_obj = CheckError.CheckError(
            rule_id=rule_id,
            description=description,
            level=level
        )
        self.storage[rule_id] = error_obj

    def remove_error(self, rule_id):
        if rule_id in self.storage.keys():
            return self.storage.pop(rule_id)

    def clear_storage(self):
        self.storage = {}

    def dump(self):
        dump = []
        for rule_id, error_obj in self.storage.items():
            dump.append({
                'level': error_obj.level,
                'description': error_obj.description
            })
        return dump

    def sort(self):
        sorted_storage = sorted(self.storage.items(),
                                key=lambda item: item[1].level,
                                reverse=True)
        self.storage = dict(sorted_storage)

    def add_always_ids(self, user_rules):
        for rule in user_rules:
            self.always_ids.append(rule.id)

    def reset_except_always(self):
        error_keys = list(self.storage.keys())
        for error_id in error_keys:
            if error_id in self.always_ids:
                continue
            self.storage.pop(error_id)
