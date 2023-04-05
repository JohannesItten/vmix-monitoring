import aiohttp
import asyncio
import sys
from time import time

import json

import websockets

import VmixState as VS

WS_SERVER_URI = ""
vmix_states = {}


def read_config(filename):
    config = None
    with open(filename, "r", encoding="utf-8") as file:
        config = json.load(file)

    for param in config['vmixes']:
        state = VS.VmixState(param["ip"], param["name"])
        vmix_states[state.id] = state


def read_args(args):
    for i in range(0, len(args), 2):
        param = args[i]
        val = args[i + 1]
        if param == "-ws":
            global WS_SERVER_URI
            WS_SERVER_URI = val
            
            
def check_params():
    is_params_ok = True
    
    if not WS_SERVER_URI:
        print("\nAdd websocket server URI with -ws arg\n")
        is_params_ok = False
    
    return is_params_ok
    

async def send_state(vmix_id, state_level, state):
    async with websockets.connect(WS_SERVER_URI) as connect:
        client_info = {"type": "update", "id": vmix_id, "state_level": state_level, "state": state}
        await connect.send(json.dumps(client_info))


async def process_api_response(vmix_id, response):
    state = vmix_states[vmix_id]
    state.updateState(response)
    if state.is_changed:
        vmix_states[vmix_id] = state
        await send_state(vmix_id, state.level, state.state)


async def get_api_response(vmix_id, ip, session):
    try:
        url = "http://{}:8088/api".format(ip)
        async with session.get(url) as response:
            resp = await response.read()
            await process_api_response(vmix_id, resp)
    except aiohttp.ClientConnectorError:
        print("Unresolved: {}".format(ip))
        await send_state(vmix_id, 3, None)
    except asyncio.TimeoutError:
        print("Timeout: {}".format(ip))
        await send_state(vmix_id, 3, None)


async def main():
    tasks = []
    timeout = aiohttp.ClientTimeout(total=20, connect=1)
    repeat_every = 1
    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            time_start = time()
            for state in vmix_states.values():
                task = asyncio.create_task(get_api_response(state.id, state.ip, session))
                tasks.append(task)
        
            await asyncio.gather(*tasks, return_exceptions=True)
            print("\nTime passed:", time() - time_start)
            tasks.clear()
            await asyncio.sleep(repeat_every)


if __name__ == "__main__":
    read_config("vmixes.json")
    read_args(sys.argv[1:])
    
    if not check_params():        
        sys.exit(1)
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server...\n")
        sys.exit()
