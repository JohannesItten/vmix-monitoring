import asyncio
import aiohttp
from time import time
import json
import websockets
import sys
import common.ConfigReader as ConfigReader
from gotify import Gotify

_gotify = None


class MonitorServer:

    def __init__(self, delay: int, vmixes_config: str, rules_config: str, websocket_uri: str):
        self.vmixes = None
        self.repeat_every = delay
        self.vmixes_config = vmixes_config
        self.rules_config = rules_config
        self.websocket_uri = websocket_uri
        self.user_rules = {}
        self.__init_gotify()

    def __read_configs(self):
        reader = ConfigReader.ConfigReader()
        self.user_rules = reader.read_rules('rules.yaml')
        self.vmixes = reader.read_vmixes('vmixes.yaml')

    def run(self):
        self.__read_configs()
        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt:
            print("\nShutting down server...\n")
            sys.exit()

    async def __main(self):
        await self.__notify('Monitoring has been started',
                            'monitor-server')
        tasks = []
        timeout = aiohttp.ClientTimeout(total=3, connect=1)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while True:
                time_start = time()
                for vmix_id in self.vmixes:
                    task = asyncio.create_task(self.__get_api_response(session, vmix_id))
                    tasks.append(task)
                await asyncio.gather(*tasks, return_exceptions=False)
                print("\nParsing cycle time:", time() - time_start)
                tasks.clear()
                await asyncio.sleep(self.repeat_every)

    async def __get_api_response(self, session, vmix_id):
        vmix = self.vmixes[vmix_id]
        try:
            async with session.get(vmix.api_uri) as response:
                api_xml = await response.read()
                await self.__process_api_response(api_xml, vmix_id)
        except (aiohttp.InvalidURL,
                aiohttp.ClientConnectorError,
                aiohttp.ServerTimeoutError):
            await self.__send_error(vmix_id,
                                    "Can't connect to {}".format(vmix.api_uri))

    async def __process_api_response(self, api_xml, vmix_id):
        vmix = self.vmixes[vmix_id]
        vmix.process_xml_snapshot(api_xml, self.user_rules[vmix.rule_name])
        await self.__send_state(vmix_id)
        if vmix.state.is_online_changed:
            await self.__notify_vmix_state_changed(vmix.name, vmix.state.online)
        await self.__notify_errors(vmix.name,
                                   fixed_errors=vmix.state.fixed_errors,
                                   new_errors=vmix.new_errors)
        vmix.new_errors = []

    async def __send_state(self, vmix_id):
        vmix = self.vmixes[vmix_id]
        try:
            async with websockets.connect(self.websocket_uri) as connect:
                client_info = {'type': 'update',
                               'id': vmix_id,
                               'name': vmix.name,
                               'isOnline': vmix.state.online,
                               'errors': vmix.state.errors.dump(),
                               'message': vmix.state.snapshot_dump}
                await connect.send(json.dumps(client_info))
        except ConnectionRefusedError:
            print('__send_state', "Can't connect to ws server")

    async def __send_error(self, vmix_id, error_text):
        vmix = self.vmixes[vmix_id]
        try:
            async with websockets.connect(self.websocket_uri) as connect:
                client_info = {'type': 'error',
                               'id': vmix_id,
                               'name': vmix.name,
                               'isOnline': False,
                               'message': {
                                   'text': error_text,
                                   'reason': 'monitor',
                                   'type': 'error'
                               }}
                await connect.send(json.dumps(client_info))
        except ConnectionRefusedError:
            print('__send_error', "Can't connect to ws server")

    @staticmethod
    def __init_gotify():
        global _gotify
        _gotify = Gotify(
            base_url="http://91.142.78.241",
            app_token="ArQKD_HeHW5UCUq",
        )

    @staticmethod
    async def __notify(title, message, priority=0):
        global _gotify
        if _gotify is None:
            return
        _gotify.create_message(
            message,
            title=title,
            priority=priority,
        )

    async def __notify_errors(self, vmix_name, fixed_errors, new_errors):
        for error in fixed_errors:
            message = f'fixed: "{error.description}"'
            title = f'FIX in {vmix_name}'
            await self.__notify(title, message)
        for error in new_errors:
            message = f'{error.description}'
            title = f'ERROR in {vmix_name}'
            await self.__notify(title, message)

    async def __notify_vmix_state_changed(self, vmix_name, is_online):
        is_online_text = 'online' if is_online else 'offline'
        await self.__notify(title=f'{vmix_name}',
                            message=f'{vmix_name} is {is_online_text}')
