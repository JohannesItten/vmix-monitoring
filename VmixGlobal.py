class VmixGlobal:


    def __init__(self, globals: dict):
        self.globals = globals


    def get_value(self, name):
        if name not in self.globals.keys(): return None
        value = self.globals[name]["value"]
        try:
            value = eval(value)
        except (SyntaxError, TypeError, NameError):
            pass
        return value


    def get_props(self, name):
        if name not in self.globals.keys(): return None
        return self.globals[name]["props"]