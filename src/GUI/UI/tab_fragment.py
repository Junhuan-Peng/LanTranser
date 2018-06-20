# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_fragment.ui',
# licensing of 'tab_fragment.ui' applies.
#
# Created: Tue Jun 19 23:34:36 2018
#      by: pyside2-uic  running on PySide2 5.11.0a1.dev1528475199
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(628, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.msgListView = QtWidgets.QListView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msgListView.sizePolicy().hasHeightForWidth())
        self.msgListView.setSizePolicy(sizePolicy)
        self.msgListView.setWordWrap(True)
        self.msgListView.setObjectName("msgListView")
        self.verticalLayout_2.addWidget(self.msgListView)
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.msgTEd = QtWidgets.QPlainTextEdit(self.frame)
        self.msgTEd.setObjectName("msgTEd")
        self.horizontalLayout.addWidget(self.msgTEd)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sendFileBtn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendFileBtn.sizePolicy().hasHeightForWidth())
        self.sendFileBtn.setSizePolicy(sizePolicy)
        self.sendFileBtn.setObjectName("sendFileBtn")
        self.verticalLayout.addWidget(self.sendFileBtn)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.sendMsgBtn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendMsgBtn.sizePolicy().hasHeightForWidth())
        self.sendMsgBtn.setSizePolicy(sizePolicy)
        self.sendMsgBtn.setObjectName("sendMsgBtn")
        self.verticalLayout.addWidget(self.sendMsgBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.sendFileBtn.setText(QtWidgets.QApplication.translate("Form", "发送文件", None, -1))
        self.sendMsgBtn.setText(QtWidgets.QApplication.translate("Form", "发送消息", None, -1))

