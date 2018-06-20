import re
import socket
from collections import deque
from threading import Thread

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Slot, Signal

from src.GUI.TabFragment import TabFragment
from src.GUI.UI.main_window import Ui_MainWindow
from src.NET.Broadcast import BroadcastListener, BroadcastSender
from src.NET.FileTransfer import FileReceiver, FileSender


class MainWindow(QtWidgets.QMainWindow):
    file_send_ack_signal = Signal(str)  # 确认发送文件信号，开启服务端
    file_send_ref_signal = Signal(str)  # 停止发送文件信号

    file_receive_ack_signal = Signal((str, str))  # 文件接受确认信号
    file_receive_ref_signal = Signal(str)  # 文件接收拒绝信号

    new_data_to_resolve_signal=Signal(str)  # 从消息队列中拿到新数据

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.file_receive_ack_signal.connect(self.__send_file_ack_msg)
        self.file_receive_ref_signal.connect(self.__send_file_ref_msg)
        self.new_data_to_resolve_signal.connect(self.__data_resolve)

        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.__on_tab_closed)
        self.__table_view_init()
        self.__broadcastListener = BroadcastListener()
        self.__broadcastListener.newDataSignal.connect(self.__add_new_data)
        self.__msg_queue: deque[str] = deque()
        self.__broadcastSender = BroadcastSender()

        self.__login()
        self.__listen()

        self.__files = deque()  # 待发送的文件列表
        self.file_send_ack_signal.connect(self.start_file_transfer)

    @property
    def table_view(self):
        return self.__ui.contactTableView

    @property
    def tab_widget(self):
        return self.__ui.tabWidget

    @property
    def ui(self):
        return self.__ui

    def __add_fragment(self):

        row = self.table_view.currentIndex().row()
        model = self.table_view.model()
        name = model.data(model.index(row, 0))
        ip = model.data(model.index(row, 1))

        size = self.tab_widget.count()
        for i in range(size):
            text = self.tab_widget.tabToolTip(i)
            if text == ip:
                self.tab_widget.setCurrentIndex(i)
                break
        else:
            tab = TabFragment(name, ip)
            tab.sendSignal.connect(self.__send_msg)
            tab.sendFileREQSignal.connect(self.__send_file_req_msg)
            tab.fileSelectedSignal.connect(self.__new_file_select)
            self.file_send_ref_signal.connect(tab.end_file_transfer)
            self.tab_widget.addTab(tab, name)
            self.tab_widget.setTabToolTip(self.tab_widget.count() - 1, ip)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    @Slot(int)
    def __on_tab_closed(self, i: int):
        self.tab_widget.removeTab(i)

    @Slot(str)
    def __add_new_data(self, data: str):
        self.__msg_queue.append(data)

    def __table_view_init(self):
        model = QtGui.QStandardItemModel(self.table_view)
        model.setHorizontalHeaderLabels(["Name", "IP"])  # 添加表头
        self.table_view.setModel(model)
        # 设置表头单元格同内容同款
        self.table_view.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # 设置表头单元格填充空白区域
        self.table_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # 设置内容居中
        self.table_view.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        # 按行选中
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 双击item打开new tab
        self.table_view.doubleClicked.connect(self.__add_fragment)

        self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_view.setAutoFillBackground(True)

    def __add_contact(self, name, ip):

        model: QtGui.QStandardItemModel = self.table_view.model()
        rows = model.rowCount()

        #  匹配已存在联系人
        for i in range(rows):
            if model.data(model.index(i, 1)) == ip:
                model.removeRow(i)
                model.insertRow(i, [QtGui.QStandardItem(name), QtGui.QStandardItem(ip)])
                break
        else:  # 联系人不存在
            model.appendRow([QtGui.QStandardItem(name), QtGui.QStandardItem(ip)])

        #  判断是否是自己
        my_name = socket.gethostname()
        my_ip = socket.gethostbyname(name)  #
        if ip != my_ip:  # 如果不是自己，则向对方发送自己的信息
            self.__broadcastSender.send(f'{my_name}##{my_ip}##I', ip=ip)

    def __remove_contact(self, ip):
        model: QtGui.QStandardItemModel = self.table_view.model()
        rows = model.rowCount()
        for i in range(rows):
            if model.data(model.index(i, 1)) == ip:
                model.removeRow(i)
                break

    def __listen(self):
        a = Thread(target=self.__broadcastListener.run, args=[self.__msg_queue])
        a.setDaemon(True)
        a.start()
        b = Thread(target=self.__update)
        b.setDaemon(True)
        b.start()

    def __update(self):
        import time
        while True:
            msg_queue_size = len(self.__msg_queue)
            if msg_queue_size != 0:
                print(self.__msg_queue)
                for i in range(msg_queue_size):
                    temp = self.__msg_queue.popleft()
                    print(f'popleft:{temp}')

                    self.new_data_to_resolve_signal.emit(temp)

            time.sleep(0.1)

    @Slot(str)
    def __data_resolve(self, data: str):
        try:
            # 匹配登录(Name##IP##I)
            match_result = re.match(r'^(.+)##((?:\d+.){3}(?:\d+))##I$', data)
            if match_result is not None:
                name = match_result.group(1)  # name
                ip = match_result.group(2)  # ip
                print(f'IP:{ip}, Name:{name}')
                self.__add_contact(name, ip)
                return

            # 匹配登录(Name##IP##O)
            match_result = re.match(r'^(.+)##((?:\d+.){3}(?:\d+))##O$', data)
            if match_result is not None:
                ip = match_result.group(2)  # ip
                self.__remove_contact(ip)
                return

            # 匹配信息接受
            match_result = re.match(r'^MSG##((?:\d+.){3}(?:\d+))##(.+)$', data)
            if match_result is not None:
                src_ip = match_result.group(1)
                text = match_result.group(2)
                self.__receive_msg(src_ip, text)
                return
            # 匹配文件发送请求
            match_result = re.match(r'^REQ##(.+)##((?:\d+.){3}(?:\d+))##(.+)$', data)
            if match_result is not None:
                src_name = match_result.group(1)
                src_ip = match_result.group(2)
                file_name = match_result.group(3)

                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setText(f"是否接受来自{src_name}的文件{file_name}")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgBox.setDetailedText(f"IP:{src_ip}")
                ret = msgBox.exec()

                my_name = socket.gethostname()
                my_ip = socket.gethostbyname(my_name)

                if ret == QtWidgets.QMessageBox.Ok:
                    #  接受
                    #  向对方发送“确认接收文件”信息
                    self.file_receive_ack_signal.emit(src_ip, file_name)

                else:
                    #  拒绝
                    #  向对方发送“拒绝接受文件”信息
                    self.file_receive_ref_signal.emit(src_ip)

                return

            # 匹配接收文件传输同意消息——收到对方同意接收信号消息
            match_result = re.match(r'^ACK##((?:\d+.){3}(?:\d+))$', data)
            if match_result:
                ip = match_result.group(1)
                self.file_send_ack_signal.emit(ip)  # 确认发送文件
            # 匹配接收文件拒绝消息
            match_result = re.match(r'^REF##((?:\d+.){3}(?:\d+))$', data)
            if match_result:
                ip = match_result.group(1)
                self.file_send_ref_signal.emit(ip)

        except Exception as e:
            print(e)

    def __login(self):
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        self.__broadcastSender.send(f'{name}##{ip}##I')

    def __logout(self):
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        self.__broadcastSender.send(f'{name}##{ip}##O')

    @Slot(str, str)
    def __send_msg(self, ip, data):
        myname = socket.gethostname()
        myip = socket.gethostbyname(myname)
        self.__broadcastSender.send(f'MSG##{myip}##{data}', ip=ip)

    @Slot(str, str)
    def __send_file_req_msg(self, goal_ip, filename):
        '''
        发送“发送文件请求”消息
        :param goal_ip:
        :param filename:
        :return:
        '''
        myname = socket.gethostname()
        myip = socket.gethostbyname(myname)
        self.__broadcastSender.send(f'REQ##{myname}##{myip}##{filename}', ip=goal_ip)

    @Slot(str, str)
    def __send_file_ack_msg(self, goal_ip: str, file_name: str):
        '''
        向对方发送“同意接受文件信号”， 并开启客户端
        :param goal_ip:
        :param file_name:
        :return:
        '''
        myname = socket.gethostname()
        myip = socket.gethostbyname(myname)
        self.__broadcastSender.send(f"ACK##{myip}", ip=goal_ip)
        import time
        time.sleep(2)  # 等待2秒，避免服务器还未打开
        file_receiver = FileReceiver(goal_ip, file_name)
        a = Thread(target=file_receiver.run)
        a.setDaemon(True)
        a.start()


    @Slot(str)
    def __send_file_ref_msg(self, goal_ip: str):
        myname = socket.gethostname()
        myip = socket.gethostbyname(myname)
        self.__broadcastSender.send(f"REF##{myip}", ip=goal_ip)

    def __receive_msg(self, ip, data):
        size = self.tab_widget.count()
        #  寻找联系人是否打开
        for i in range(size):
            text = self.tab_widget.tabToolTip(i)
            if text == ip:
                self.tab_widget.setCurrentIndex(i)
                tab: TabFragment = self.tab_widget.widget(i)
                tab.receive_msg(data)
                break
        else:  # 如果没有，则从table中找到数据，创建新的tab
            model: QtGui.QStandardItemModel = self.table_view.model()
            rows = model.rowCount()
            name = ''
            for i in range(rows):
                if model.data(model.index(i, 1)) == ip:
                    name = model.data(model.index(i, 0))
                    break
            else:  # 不存在该联系人
                return

            tab = TabFragment(name, ip)
            self.tab_widget.addTab(tab, name)
            self.tab_widget.setTabToolTip(self.tab_widget.count() - 1, ip)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            self.file_send_ref_signal.connect(tab.end_file_transfer)
            tab.fileSelectedSignal.connect(self.__new_file_select)
            tab.sendSignal.connect(self.__send_msg)
            tab.sendFileREQSignal.connect(self.__send_file_req_msg)
            tab.receive_msg(data)

    def close(self, *args, **kwargs):
        self.__logout()
        self.__broadcastSender.close()
        self.__broadcastListener.close()
        super().close(*args, **kwargs)

    @Slot(str, str)
    def __new_file_select(self, goal_ip, file_path):
        print(f"MainWin: 文件{file_path}发往{goal_ip}添加进文件队列")
        self.__files.append((goal_ip, file_path))

    @Slot(str)
    def start_file_transfer(self, goal_ip: str):
        print(f"{goal_ip}同意接收文件")
        for i, (ip, file_path) in enumerate(self.__files):
            if ip == goal_ip:
                self.__files.remove((ip, file_path))
                file_sender = FileSender(file_path)
                a = Thread(target=file_sender.run)
                a.setDaemon(True)
                a.start()
                break