import websocket.WebsocketServer as WebsocketServer


def main():
    websocket_server = WebsocketServer.WebsocketServer(
        host='0.0.0.0',
        port='9090',
        is_global=False,
        is_mustdie=False
    )
    websocket_server.run()


if __name__ == '__main__':
    main()
