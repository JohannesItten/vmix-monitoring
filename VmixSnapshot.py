import VmixInput
import VmixGlobal


class VmixSnapshot:
    def __init__(self, vmix_global: VmixGlobal,
                 buses: dict,
                 active_input: VmixInput,
                 inputs: dict,
                 overlays: dict,
                 mixes: dict):
        self.vmix_global = vmix_global
        self.active_input = active_input
        self.buses = buses
        self.inputs = inputs
        self.overlays = overlays
        self.mixes = mixes

    def dump(self):
        vmix_global = self.vmix_global.dump()
        active = self.vmix_global.dump()
        buses = []
        for short_name, bus in self.buses.items():
            buses.append(bus.dump())
        inputs = []
        for user_key, vmix_input in self.inputs.items():
            inputs.append(vmix_input.dump())
        overlays = {}
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
            'overlays': {},
            'mixes': mixes
        }
