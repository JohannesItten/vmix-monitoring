from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import control.DaemonUnit as DaemonUnit

templates = Jinja2Templates(directory="vue")
app = FastAPI()
app.mount("/assets", StaticFiles(directory="vue/assets"), name="assets")
app.mount("/favicon", StaticFiles(directory="vue/favicon"), name="favicon")

# TODO read from config
_WS_SERVER = 'ws://localhost:9090'
_WS_UNIT_NAME = 'ws-monitor'
_MON_UNIT_NAME = 'vmix-monitor'

_ws_unit = DaemonUnit.DaemonUnit(_WS_UNIT_NAME)
_mon_unit = DaemonUnit.DaemonUnit(_MON_UNIT_NAME)


@app.get('/api/defaults')
async def defaults():
    return {
        'server': _WS_SERVER
    }


@app.get("/api/service/state")
async def get_service(request: Request):
    return {
        'ws': _ws_unit.get_state(),
        'monitor': _mon_unit.get_state()
    }


@app.get("/api/service/restart")
async def restart_all(request: Request):
    result = (_ws_unit.stop_service()
              + _mon_unit.stop_service()
              + _ws_unit.start_service()
              + _mon_unit.start_service())
    return {
        'isError': result != 4
    }
