import socket


class FileTransferManager:
    pass


class FileReceiver:
    def __init__(self, ip, file_path):
        self.__client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__ip = ip
        self.__file_path = file_path

    def run(self):
        count = 10
        while True:
            try:
                self.__client.connect((self.__ip, 5555))
                with open(self.__file_path, "ab") as f:
                    while True:
                        data = self.__client.recv(1024)
                        if not data:
                            break
                        f.write(data)
                self.__client.close()
                print('接收完毕')
                return
            except Exception as _:
                import time
                time.sleep(0.2)
                count = count - 1
                if count < 0:
                    print("异常过多，终止接收")
                    return


class FileSender:
    def __init__(self, file_path: str):
        self.__soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 固定端口号
        self.__soc.bind(("", 5555))
        self.__soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 将主动套接字转为被动套接字
        self.__soc.listen(3)
        self.__file_path = file_path

    def run(self):
        print("等待连接……")
        skt, addr = self.__soc.accept()
        print(f'与{addr}连接')
        with open(self.__file_path, 'rb') as f:
            for data in f:
                skt.send(data)
        skt.close()
        self.__soc.close()
        print("发送完毕")

