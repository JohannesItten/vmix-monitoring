import os
import subprocess


class DaemonUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name

    def get_state(self):
        result = subprocess.call(
            ['systemctl',
             'is-active',
             '--user',
             '--quiet',
             self.unit_name],
            shell=False
        )
        return True if result == 0 else False

    def stop_service(self):
        result = subprocess.call(
            ['systemctl',
             'stop',
             '--user',
             '--quiet',
             self.unit_name],
            shell=False
        )
        return True if result == 0 else False

    def start_service(self):
        result = subprocess.call(
            ['systemctl',
             'start',
             '--user',
             '--quiet',
             self.unit_name],
            shell=False
        )
        return True if result == 0 else False

