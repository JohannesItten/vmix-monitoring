import asyncio
import json

import websockets
import os
from sys import exit
from signal import signal, SIGINT, SIGTERM


watchers = set()


def exit_handler(signal_recieved, frame):
    print("\nShutting down server...\n")
    exit(0)


async def watch(websocket):
    watchers.add(websocket)
    await websocket.send(json.dumps("Hello!"))
    await asyncio.Event().wait()


async def broadcast_to_watchers(message):
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
    loop.add_signal_handler(SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "9090"))
    async with websockets.serve(handler, "localhost", port):
        await asyncio.Future()


if __name__ == "__main__":
    signal(SIGINT, exit_handler)
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
