from common.check_error import CheckError


class CheckErrorStorage:
    def __init__(self):
        self.storage = {}

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