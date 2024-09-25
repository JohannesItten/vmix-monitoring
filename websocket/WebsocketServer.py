import asyncio
import functools
import json
import sys

import websockets
import os
import common.ConfigReader as ConfigReader
import signal
from websocket import wskiller


class WebsocketServer:
    def __init__(self,
                 host: str,
                 port: str,
                 is_global: bool = False,
                 is_debug: bool = False):
        self.host = host
        self.port = port
        self.is_global = is_global
        self.is_debug = is_debug

        self.watchers = set()
        self.vmixes_init_info = []
        self.__read_configs()

    def run(self):
        asyncio.run(self.__main())

    async def __watch(self, websocket, watcher_page):
        self.watchers.add(websocket)
        await websocket.send(json.dumps({
            'type': 'init',
            'message': self.__get_page(9, watcher_page)
        }))
        try:
            await websocket.wait_closed()
        finally:
            print('watcher removed')
            self.watchers.remove(websocket)
        # await asyncio.Event().wait()

    async def __broadcast_to_watchers(self, message):
        websockets.broadcast(self.watchers, message)

    async def __message_handler(self, websocket):
        try:
            message = await websocket.recv()
            if wskiller.kill_now():
                sys.exit(0)
            action = json.loads(message)
        except websockets.exceptions.ConnectionClosed:
            print('conn is closed')
            return

        if 'watch' in action['type']:
            print('watcher connected')
            watcher_page = 1
            if 'page' in action['payload']:
                watcher_page = action['payload']['page']
            await self.__watch(websocket, watcher_page)
        elif 'update' or 'error' in action['type']:
            await self.__broadcast_to_watchers(message)

    async def __main(self):
        loop = asyncio.get_running_loop()
        for signal_name in {'SIGTERM', 'SIGINT'}:
            loop.add_signal_handler(
                getattr(signal, signal_name),
                functools.partial(self.__exit_handler, signal_name, loop)
            )
        if self.is_debug:
            port = int(os.environ.get('PORT', self.port))
            async with websockets.serve(self.__message_handler, self.host, port):
                await asyncio.Future()
        else:
            print('PATH', f"/var/run/{os.environ['SUPERVISOR_PROCESS_NAME']}.sock")
            async with websockets.unix_serve(
                    self.__message_handler,
                    path=f"/var/run/{os.environ['SUPERVISOR_PROCESS_NAME']}.sock"
            ):
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

    def __get_page(self, page_amount, page_number=1):
        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 1
        vmixes = self.vmixes_init_info
        page_vmixes_max = min([len(vmixes), page_amount * page_number])

        page_vmixes = []
        for i in range(page_number * page_amount - page_amount, page_vmixes_max):
            page_vmixes.append(vmixes[i])
        return page_vmixes

    @staticmethod
    def __exit_handler(signal_name, loop):
        loop.stop()
        sys.exit(0)
