import websocket.WebsocketServer as WebsocketServer


def main():
    websocket_server = WebsocketServer.WebsocketServer(
        host='localhost',
        port='9090',
        is_global=False
    )
    websocket_server.run()


if __name__ == '__main__':
    main()
