# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui',
# licensing of 'main_window.ui' applies.
#
# Created: Tue Jun 19 15:48:50 2018
#      by: pyside2-uic  running on PySide2 5.11.0a1.dev1528475199
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.contactTableView = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contactTableView.sizePolicy().hasHeightForWidth())
        self.contactTableView.setSizePolicy(sizePolicy)
        self.contactTableView.setMaximumSize(QtCore.QSize(217, 16777215))
        self.contactTableView.setProperty("cursor", QtCore.Qt.ArrowCursor)
        self.contactTableView.setMouseTracking(False)
        self.contactTableView.setAutoFillBackground(True)
        self.contactTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.contactTableView.setObjectName("contactTableView")
        self.horizontalLayout.addWidget(self.contactTableView)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit_Q = QtWidgets.QAction(MainWindow)
        self.actionQuit_Q.setObjectName("actionQuit_Q")
        self.actionshow = QtWidgets.QAction(MainWindow)
        self.actionshow.setObjectName("actionshow")
        self.actionadd = QtWidgets.QAction(MainWindow)
        self.actionadd.setObjectName("actionadd")
        self.menuFile.addAction(self.actionQuit_Q)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.actionQuit_Q, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.actionQuit_Q.setText(QtWidgets.QApplication.translate("MainWindow", "Quit(&Q)", None, -1))
        self.actionshow.setText(QtWidgets.QApplication.translate("MainWindow", "show", None, -1))
        self.actionadd.setText(QtWidgets.QApplication.translate("MainWindow", "add", None, -1))

