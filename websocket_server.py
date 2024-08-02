import asyncio
import json
import websockets
import os
import sys
from signal import signal, SIGINT, SIGTERM
import config.ConfigReader as ConfigReader

SERVER_HOST = 'localhost'
SERVER_PORT = '9090'
IS_MUSTDIE = False

watchers = set()

# TODO: store states in redis
vmixes_init_info = []


def exit_handler(signal_received, frame):
    print('\nShutting down server...\n')
    sys.exit(0)


async def watch(websocket):
    watchers.add(websocket)
    await websocket.send(json.dumps({
            'type': 'init',
            'message': vmixes_init_info
         }))
    try:
        await websocket.wait_closed()
    finally:
        print('watcher removed')
        watchers.remove(websocket)
    # await asyncio.Event().wait()


async def broadcast_to_watchers(message):
    state = json.loads(message)
    websockets.broadcast(watchers, message)


async def handler(websocket):
    try:
        message = await websocket.recv()
        action = json.loads(message)
    except websockets.exceptions.ConnectionClosed:
        print('conn is closed')
        return

    if 'watch' in action['type']:
        print('watcher connected')
        print(action['payload']['page'])
        await watch(websocket)
    elif 'update' or 'error' in action['type']:
        await broadcast_to_watchers(message)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    if not IS_MUSTDIE:
        loop.add_signal_handler(SIGTERM, stop.set_result, None)

    port = int(os.environ.get('PORT', SERVER_PORT))
    async with websockets.serve(handler, SERVER_HOST, port):
        await asyncio.Future()


def read_configs():
    reader = ConfigReader.ConfigReader()
    vmixes = reader.read_vmixes_ws('vmixes.yaml')
    front_views = reader.read_front('front.yaml')
    for vmix in vmixes:
        user_rule = vmix['rule']
        if user_rule not in front_views:
            front_views[user_rule] = None
        vmixes_init_info.append({
            'id': vmix['id'],
            'name': vmix['name'],
            'view': front_views[user_rule],
        })


if __name__ == '__main__':
    read_configs()
    signal(SIGINT, exit_handler)
    if IS_MUSTDIE:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
