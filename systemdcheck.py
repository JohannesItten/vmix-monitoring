from pystemd.systemd1 import Unit
unit = Unit(b'dhcpcd.service')
unit.load()

active_state = unit.Unit.ActiveState
is_active = True if active_state == b'active' else False
print(is_active)
