# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Code\Python\MiniChat\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_conn = QtWidgets.QHBoxLayout()
        self.layout_conn.setObjectName("layout_conn")
        self.ledit_addr = LineEdit(self.centralwidget)
        self.ledit_addr.setObjectName("ledit_addr")
        self.layout_conn.addWidget(self.ledit_addr)
        self.sbox_port = SpinBox(self.centralwidget)
        self.sbox_port.setMaximum(65535)
        self.sbox_port.setProperty("value", 9898)
        self.sbox_port.setObjectName("sbox_port")
        self.layout_conn.addWidget(self.sbox_port)
        self.btn_conn = PushButton(self.centralwidget)
        self.btn_conn.setObjectName("btn_conn")
        self.layout_conn.addWidget(self.btn_conn)
        self.verticalLayout.addLayout(self.layout_conn)
        self.layout_login = QtWidgets.QVBoxLayout()
        self.layout_login.setObjectName("layout_login")
        self.ledit_account = LineEdit(self.centralwidget)
        self.ledit_account.setObjectName("ledit_account")
        self.layout_login.addWidget(self.ledit_account)
        self.ledit_password = LineEdit(self.centralwidget)
        self.ledit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledit_password.setObjectName("ledit_password")
        self.layout_login.addWidget(self.ledit_password)
        self.ledit_passwordre = LineEdit(self.centralwidget)
        self.ledit_passwordre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledit_passwordre.setObjectName("ledit_passwordre")
        self.layout_login.addWidget(self.ledit_passwordre)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_login = PushButton(self.centralwidget)
        self.btn_login.setEnabled(False)
        self.btn_login.setObjectName("btn_login")
        self.horizontalLayout.addWidget(self.btn_login)
        self.btn_register = PushButton(self.centralwidget)
        self.btn_register.setEnabled(False)
        self.btn_register.setObjectName("btn_register")
        self.horizontalLayout.addWidget(self.btn_register)
        self.layout_login.addLayout(self.horizontalLayout)
        self.layout_login.setStretch(0, 1)
        self.layout_login.setStretch(1, 1)
        self.layout_login.setStretch(2, 1)
        self.verticalLayout.addLayout(self.layout_login)
        self.btn_enter = PrimaryPushButton(self.centralwidget)
        self.btn_enter.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_enter.sizePolicy().hasHeightForWidth())
        self.btn_enter.setSizePolicy(sizePolicy)
        self.btn_enter.setProperty("hasIcon", True)
        self.btn_enter.setObjectName("btn_enter")
        self.verticalLayout.addWidget(self.btn_enter)
        self.IndeterminateProgressBar = IndeterminateProgressBar(self.centralwidget)
        self.IndeterminateProgressBar.setEnabled(True)
        self.IndeterminateProgressBar.setProperty("value", 0)
        self.IndeterminateProgressBar.setTextVisible(True)
        self.IndeterminateProgressBar.setObjectName("IndeterminateProgressBar")
        self.verticalLayout.addWidget(self.IndeterminateProgressBar)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ledit_addr.setPlaceholderText(_translate("MainWindow", "服务器地址"))
        self.btn_conn.setText(_translate("MainWindow", "连接"))
        self.ledit_account.setPlaceholderText(_translate("MainWindow", "账号"))
        self.ledit_password.setPlaceholderText(_translate("MainWindow", "密码"))
        self.ledit_passwordre.setPlaceholderText(_translate("MainWindow", "重复密码（注册）"))
        self.btn_login.setText(_translate("MainWindow", "登录"))
        self.btn_register.setText(_translate("MainWindow", "注册"))
        self.btn_enter.setText(_translate("MainWindow", "进入聊天室！！"))
from qfluentwidgets import IndeterminateProgressBar, LineEdit, PrimaryPushButton, PushButton, SpinBox
