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
