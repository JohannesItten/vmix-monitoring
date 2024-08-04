import math


class VmixBus:
    PROP_NOT_FOUND = None
    PROP_AMPLITUDE = "meterF"
    MASTER_NAME = "master"

    def __init__(self, name: str,
                 is_muted: bool,
                 volume_bar: float,
                 props: dict):
        self.name = name
        self.is_muted = is_muted
        self.volume_bar = volume_bar
        self.props = props

        self.short_name = self.__get_bus_short_name(name)
        self.dbfs = self.__get_dbfs()
        self.volume = self.__get_volume()

    def dump(self):
        dump = {}
        for key, attr in self.__dict__.items():
            dump[key] = attr
        return dump

    def get_prop(self, prop):
        if prop not in self.props:
            return self.PROP_NOT_FOUND
        return self.props[prop]

    def __get_bus_short_name(self, name):
        if self.MASTER_NAME in name:
            return "M"
        return name[-1:]

    # https://www.vmix.com/knowledgebase/article.aspx/144/vmix-api-audio-levels
    def __get_dbfs(self) -> list:
        amplitude = self.get_prop(self.PROP_AMPLITUDE)
        if type(amplitude) is not dict:
            return []
        dbfs = []
        for key, amp in amplitude.items():
            amp = float(amp)
            if amp <= 0:
                # -inf
                dbfs.append(-10000)
                continue
            dbfs_val = 20 * math.log10(amp)
            dbfs.append(round(dbfs_val, 3))
        return dbfs

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
