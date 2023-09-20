import asyncio
import json

import websockets
import os
import sys
from signal import signal, SIGINT, SIGTERM


SERVER_HOST = "localhost"
IS_MUSTDIE = False

watchers = set()

#TODO: store states in db. Also check broadcast_to_watchers
vmix_states = {}


def read_args(args):
    for i in range(0, len(args), 1):
        param = args[i]
        if param == "-g":
            global SERVER_HOST
            SERVER_HOST = "0.0.0.0"
        elif param == "-win":
            global IS_MUSTDIE
            IS_MUSTDIE = True


def exit_handler(signal_recieved, frame):
    print("\nShutting down server...\n")
    exit(0)


async def watch(websocket):
    watchers.add(websocket)
    await websocket.send(json.dumps({"init": vmix_states}))
    await asyncio.Event().wait()


async def broadcast_to_watchers(message):
    state = json.loads(message)
    if "id" in state:
        vmix_states[state["id"]] = message
    websockets.broadcast(watchers, message)

async def handler(websocket):
    try:
        message = await websocket.recv()
        event = json.loads(message)
    except websockets.exceptions.ConnectionClosed:
        print("conn is closed")
        return
    
    if "watch" in event["type"]:
        await watch(websocket)
    elif "update" in event["type"]:
        await broadcast_to_watchers(message)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    if not IS_MUSTDIE: loop.add_signal_handler(SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "9090"))
    async with websockets.serve(handler, SERVER_HOST, port):
        await asyncio.Future()


if __name__ == "__main__":
    read_args(sys.argv[1:])
    signal(SIGINT, exit_handler)
    if IS_MUSTDIE: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
