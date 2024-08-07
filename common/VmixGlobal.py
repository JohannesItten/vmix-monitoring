class VmixGlobal:
    PROP_NOT_FOUND = None

    def __init__(self, vmix_globals: dict):
        self.globals = vmix_globals

    def dump(self):
        return self.globals

    def get_value(self, name):
        if name not in self.globals.keys():
            return self.PROP_NOT_FOUND
        value = self.globals[name]["value"]
        try:
            value = eval(value)
        except (SyntaxError, TypeError, NameError):
            pass
        return value

    def get_props(self, name):
        if name not in self.globals.keys():
            return self.PROP_NOT_FOUND
        return self.globals[name]["props"]
