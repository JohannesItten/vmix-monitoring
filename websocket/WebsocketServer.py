import asyncio
import json
import websockets
import os
import sys
from signal import signal, SIGINT, SIGTERM
import common.ConfigReader as ConfigReader


def exit_handler(signal_received, frame):
    print('\nShutting down server...\n')
    sys.exit(0)


class WebsocketServer:
    def __init__(self,
                 host: str,
                 port: str,
                 is_global: False,
                 is_mustdie: False):
        self.host = host
        self.port = port
        self.is_global = is_global
        self.is_mustdie = is_mustdie

        self.watchers = set()
        self.vmixes_init_info = []
        self.__read_configs()

    def run(self):
        signal(SIGINT, exit_handler)
        if self.is_mustdie:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.__main())

    async def __watch(self, websocket):
        self.watchers.add(websocket)
        await websocket.send(json.dumps({
            'type': 'init',
            'message': self.vmixes_init_info
        }))
        try:
            await websocket.wait_closed()
        finally:
            print('watcher removed')
            self.watchers.remove(websocket)
        # await asyncio.Event().wait()

    async def __broadcast_to_watchers(self, message):
        # state = json.loads(message)
        websockets.broadcast(self.watchers, message)

    async def __handler(self, websocket):
        try:
            message = await websocket.recv()
            action = json.loads(message)
        except websockets.exceptions.ConnectionClosed:
            print('conn is closed')
            return

        if 'watch' in action['type']:
            print('watcher connected')
            print(action['payload']['page'])
            await self.__watch(websocket)
        elif 'update' or 'error' in action['type']:
            await self.__broadcast_to_watchers(message)

    async def __main(self):
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        if not self.is_mustdie:
            loop.add_signal_handler(SIGTERM, stop.set_result, None)

        port = int(os.environ.get('PORT', self.port))
        async with websockets.serve(self.__handler, self.host, port):
            await asyncio.Future()

    def __read_configs(self):
        reader = ConfigReader.ConfigReader()
        vmixes = reader.read_vmixes_ws('vmixes.yaml')
        front_views = reader.read_front('front.yaml')
        for vmix in vmixes:
            user_rule = vmix['rule']
            if user_rule not in front_views:
                front_views[user_rule] = None
            self.vmixes_init_info.append({
                'id': vmix['id'],
                'name': vmix['name'],
                'view': front_views[user_rule],
            })
