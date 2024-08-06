import time

_ERROR_LEVELS = {
    'parsing': 100,
    'error': 3,
    'warning': 2,
    'info': 1
}


class CheckError:
    def __init__(self, rule_id,
                 description: str,
                 level: int):
        self.rule_id = rule_id
        self.description = description
        self.timestamp = time.time()
        self.level = _ERROR_LEVELS[level]

    def __lt__(self, other):
        return (self.level < other.level and
                self.timestamp < other.timestamp)

    def __str__(self):
        return f'{self.rule_id}: {self.description}'
