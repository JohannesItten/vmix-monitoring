from common import VmixGlobal, VmixInput


class VmixSnapshot:
    def __init__(self, vmix_global: VmixGlobal,
                 buses: dict,
                 active_input: VmixInput,
                 inputs: dict,
                 overlays: dict,
                 mixes: dict,
                 outputs: list
                 ):
        self.vmix_global = vmix_global
        self.active_input = active_input
        self.buses = buses
        self.inputs = inputs
        self.overlays = overlays
        self.mixes = mixes
        self.outputs = outputs

    def dump(self):
        vmix_global = self.vmix_global.dump()
        active = self.vmix_global.dump()
        buses = {}
        for short_name, bus in self.buses.items():
            buses[bus.name] = bus.dump()
        inputs = {}
        for user_key, vmix_input in self.inputs.items():
            inputs[user_key] = vmix_input.dump()
        overlays = {}
        for overlay_number, vmix_input in self.overlays.items():
            overlays[overlay_number] = vmix_input.dump()
        mixes = {}
        for mix_number, active_input in self.mixes.items():
            if active_input is None:
                mixes[mix_number] = None
                continue
            mixes[mix_number] = active_input.dump()
        return {
            'global': vmix_global,
            'active': active,
            'buses': buses,
            'inputs': inputs,
            'overlays': overlays,
            'mixes': mixes,
            'outputs': self.outputs
        }
