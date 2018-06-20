import socket
import sys
import traceback
from collections import deque
from PySide2 import QtCore


class BroadcastManager:
    pass


class BroadcastListener(QtCore.QObject):
    newDataSignal = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__port = 4444
        self.__socket.bind(('', self.__port))

    def run(self, container: deque = None):
        while True:
            try:
                data, addr_info = self.__socket.recvfrom(8192)
                data = str(data, encoding="utf-8")
                print(f"recieve :{data} from {addr_info}")
                if container is not None:
                    self.newDataSignal.emit(data)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                traceback.print_exc()

    def close(self):
        self.__socket.close()

class BroadcastSender:

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__port = 4444

    def send(self, data, ip=None):
        if ip is None:
            self.__socket.sendto(str(data).encode('utf-8'), ('<broadcast>', self.__port))
        else:
            try:
                self.__socket.sendto(str(data).encode('utf-8'), (ip, self.__port))
            except Exception as e:
                print(e)

    def close(self):
        self.__socket.close()

if __name__ == '__main__':
    sender = BroadcastSender()
    while True:
        x = input('Input :')
        if x == 'Quit':
            break
        sender.send(x)
    sys.exit(0)
