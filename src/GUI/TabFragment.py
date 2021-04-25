from threading import Thread

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot
from .UI.tab_fragment import Ui_Form

from src.NET.FileTransfer import FileReceiver, FileSender

class TabFragment(QtWidgets.QWidget):
    sendSignal = QtCore.Signal((str, str))  # goal_ip  msg
    sendFileREQSignal = QtCore.Signal((str, str))  # goal_ip  filename
    fileSelectedSignal = QtCore.Signal((str, str))  # goal_ip  filename

    def __init__(self, name, ip, parent=None):
        super(TabFragment, self).__init__(parent=parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)

        self.__ui.msgListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.__ui.msgListView.setViewMode(QtWidgets.QListView.ViewMode.ListMode)

        self.__model = QtGui.QStandardItemModel(self.__ui.msgListView)
        self.__ui.msgListView.setModel(self.__model)

        self.__ui.sendMsgBtn.clicked.connect(self.__on_send_msg_btn_clicked)
        self.__ui.sendFileBtn.clicked.connect(self.__on_send_file_btn_clicked)

        self.__name = name
        self.__ip = ip
        self.setToolTip(ip)
        self.__flag = False  # 记录是否有发送文件请求
        self.__files = []  # 待发送的文件列表

    def __sendMsg(self, msg, flag=False):
        temp = []
        for i in range(0, len(msg), 20):
            temp.append(msg[i:i + 20])
        msg = '\n'.join(temp)

        item = QtGui.QStandardItem(msg)
        if flag:
            item.setTextAlignment(QtCore.Qt.AlignLeft)  # 右对齐
        self.__model.appendRow(item)

        self.msg_list_view.scrollToBottom()
        self.sendSignal.emit(self.__ip, msg)

    def __on_send_msg_btn_clicked(self):
        data = self.msg_text_edit.toPlainText()
        if data is '':
            return
        self.__sendMsg(data, True)
        self.msg_text_edit.clear()

    def __on_send_file_btn_clicked(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog(), r"select file", r"~")
        if file_path is not None:
            print(f"TabFragment: 文件{file_path}发往{self.toolTip()}添加进文件队列")
            self.fileSelectedSignal.emit(self.toolTip(), file_path[0])
            file_name: str = file_path[0]
            file_name = file_name[file_name.rfind('/') + 1:]
            self.sendFileREQSignal.emit(self.toolTip(), file_name)  # 发送文件请求
            self.__flag = True

    @Slot(str)
    def end_file_transfer(self, goal_ip):
        print(f"{goal_ip}拒绝接收文件")
        self.__flag=False

    def receive_msg(self, msg: str):
        item = QtGui.QStandardItem(msg)
        self.__model.appendRow(item)
        self.msg_list_view.scrollToBottom()

    @property
    def ui(self):
        return self.__ui

    @property
    def msg_list_view(self):
        return self.ui.msgListView

    @property
    def msg_text_edit(self):
        return self.ui.msgTEd
