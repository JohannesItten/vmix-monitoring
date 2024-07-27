import math


class VmixInput:
    PROP_NOT_FOUND = None
    PROP_AMPLITUDE = 'meterF'

    def __init__(self, number: int,
                 key: str, title: str, vmix_type: str, overlays: list, texts: dict, props: dict, user_key=None):
        self.number = number
        self.key = key
        self.title = title
        self.vmix_type = vmix_type
        self.overlays = overlays
        self.texts = texts
        self.props = props
        self.user_key = user_key

    # if same key(guid) means same input
    def __eq__(self, other):
        if not isinstance(other, VmixInput):
            return False
        return self.key == other.key

    # to make sortable by input number

    def __lt__(self, other):
        if not isinstance(other, VmixInput):
            raise TypeError("Right operand must be instance of VmixInput")
        return self.number < other.number

    def __str__(self):
        return f'Input {self.number}: {self.title}'

    def get_prop(self, prop):
        if prop not in self.props:
            return self.PROP_NOT_FOUND
        return self.props[prop]

    # https://www.vmix.com/knowledgebase/article.aspx/144/vmix-api-audio-levels
    def __get_volume(self) -> list:
        amplitude = self.get_prop(self.PROP_AMPLITUDE)
        if type(amplitude) is not dict:
            return []
        volume = []
        for key, amp in amplitude.items():
            amp = float(amp)
            volume_val = math.pow(amp, 0.25) * 100
            volume.append(round(volume_val, 3))
        return volume
