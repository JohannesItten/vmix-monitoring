from monitor import MonitorServer
import time


def main():
    print('=== vMix Monitoring ===')
    print('init time:', time.time())
    monitor_server = MonitorServer.MonitorServer(delay=1,
                                                 vmixes_config='vmixes.yaml',
                                                 rules_config='rules.yaml',
                                                 websocket_uri='ws://127.0.0.1:9090')
    monitor_server.run()


if __name__ == '__main__':
    main()
