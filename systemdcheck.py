# TODO looks like better to use os.environ, due to it can't work with systemd --user scope
from pystemd.systemd1 import Unit
unit_name = b'ws-monitor.service'
unit = Unit(unit_name)
unit.load()

active_state = unit.Unit.ActiveState
is_active = True if active_state == b'active' else False
print(unit_name.decode('utf-8'), is_active)
