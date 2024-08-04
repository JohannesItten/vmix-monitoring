import time


class TimeDepCheckResult:
    def __init__(self, result_id, value):
        self.result_id = result_id
        current_time = time.time()
        self.first_update = current_time
        self.value = value
        self.delta_time = 0

    def __eq__(self, other):
        return self.result_id == other.result_id

    # Return delta time between equal value's of check function
    def update(self, new_value):
        current_time = time.time()
        if new_value == self.value:
            self.delta_time = current_time - self.first_update
            return
        self.first_update = current_time
        self.value = new_value
        self.delta_time = 0

    def reset_value(self):
        current_time = time.time()
        self.first_update = current_time
        self.value = None
