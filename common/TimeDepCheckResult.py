import time


class TimeDepCheckResult:
    def __init__(self, result_id, result):
        self.result_id = result_id
        current_time = time.time()
        self.first_update = current_time
        self.last_update = current_time
        self.result = result

    def __eq__(self, other):
        return self.result_id == other.result_id

    # Return delta time between equal result's of check function
    def update(self, new_result):
        current_time = time.time()
        if self.result != new_result:
            self.first_update = current_time
            self.last_update = current_time
            self.result = new_result
            return 0
        self.last_update = current_time
        return current_time - self.first_update

    def reset_result(self):
        current_time = time.time()
        self.first_update = current_time
        self.last_update = current_time
        self.result = None
