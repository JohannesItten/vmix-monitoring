# simple hack from official websockets gitHub repo
# https://github.com/python-websockets/websockets/issues/124
# for proper handling SIGKILL/SIGTERM from systemd
# TODO: https://github.com/python-websockets/websockets/issues/124#issuecomment-263016205
import signal

__kill_now = False


def __set_kill_now(signum, frame):
    global __kill_now
    __kill_now = True


signal.signal(signal.SIGINT, __set_kill_now)
signal.signal(signal.SIGTERM, __set_kill_now)


def kill_now() -> bool:
    global __kill_now
    return __kill_now
