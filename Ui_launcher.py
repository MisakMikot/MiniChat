# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_launcherui(object):
    def setupUi(self, launcherui):
        launcherui.setObjectName("launcherui")
        launcherui.resize(393, 236)
        self.centralwidget = QtWidgets.QWidget(launcherui)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_conn = QtWidgets.QHBoxLayout()
        self.layout_conn.setObjectName("layout_conn")
        self.ledit_addr = LineEdit(self.centralwidget)
        self.ledit_addr.setClearButtonEnabled(True)
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
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.layout_login = QtWidgets.QVBoxLayout()
        self.layout_login.setObjectName("layout_login")
        self.ledit_account = LineEdit(self.centralwidget)
        self.ledit_account.setEnabled(False)
        self.ledit_account.setClearButtonEnabled(True)
        self.ledit_account.setObjectName("ledit_account")
        self.layout_login.addWidget(self.ledit_account)
        self.ledit_password = LineEdit(self.centralwidget)
        self.ledit_password.setEnabled(False)
        self.ledit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledit_password.setClearButtonEnabled(True)
        self.ledit_password.setObjectName("ledit_password")
        self.layout_login.addWidget(self.ledit_password)
        self.ledit_passwordre = LineEdit(self.centralwidget)
        self.ledit_passwordre.setEnabled(False)
        self.ledit_passwordre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledit_passwordre.setClearButtonEnabled(True)
        self.ledit_passwordre.setObjectName("ledit_passwordre")
        self.layout_login.addWidget(self.ledit_passwordre)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_login = PushButton(self.centralwidget)
        self.btn_login.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_login.sizePolicy().hasHeightForWidth())
        self.btn_login.setSizePolicy(sizePolicy)
        self.btn_login.setObjectName("btn_login")
        self.horizontalLayout.addWidget(self.btn_login)
        self.swich_savelogin = SwitchButton(self.centralwidget)
        self.swich_savelogin.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swich_savelogin.sizePolicy().hasHeightForWidth())
        self.swich_savelogin.setSizePolicy(sizePolicy)
        self.swich_savelogin.setChecked(False)
        self.swich_savelogin.setText("")
        self.swich_savelogin.setOnText("")
        self.swich_savelogin.setOffText("")
        self.swich_savelogin.setObjectName("swich_savelogin")
        self.horizontalLayout.addWidget(self.swich_savelogin)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.btn_register = PushButton(self.centralwidget)
        self.btn_register.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_register.sizePolicy().hasHeightForWidth())
        self.btn_register.setSizePolicy(sizePolicy)
        self.btn_register.setObjectName("btn_register")
        self.horizontalLayout.addWidget(self.btn_register)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 2)
        self.layout_login.addLayout(self.horizontalLayout)
        self.layout_login.setStretch(0, 1)
        self.layout_login.setStretch(1, 1)
        self.layout_login.setStretch(2, 1)
        self.verticalLayout.addLayout(self.layout_login)
        self.IndeterminateProgressBar = IndeterminateProgressBar(self.centralwidget)
        self.IndeterminateProgressBar.setEnabled(True)
        self.IndeterminateProgressBar.setProperty("value", 0)
        self.IndeterminateProgressBar.setTextVisible(True)
        self.IndeterminateProgressBar.setObjectName("IndeterminateProgressBar")
        self.verticalLayout.addWidget(self.IndeterminateProgressBar)
        self.verticalLayout.setStretch(2, 1)
        launcherui.setCentralWidget(self.centralwidget)

        self.retranslateUi(launcherui)
        QtCore.QMetaObject.connectSlotsByName(launcherui)

    def retranslateUi(self, launcherui):
        _translate = QtCore.QCoreApplication.translate
        launcherui.setWindowTitle(_translate("launcherui", "登录-MiniChat"))
        self.ledit_addr.setPlaceholderText(_translate("launcherui", "服务器地址"))
        self.btn_conn.setText(_translate("launcherui", "连接"))
        self.ledit_account.setPlaceholderText(_translate("launcherui", "账号"))
        self.ledit_password.setPlaceholderText(_translate("launcherui", "密码"))
        self.ledit_passwordre.setPlaceholderText(_translate("launcherui", "重复密码（注册）"))
        self.btn_login.setText(_translate("launcherui", "登录"))
        self.label.setText(_translate("launcherui", "保存登录信息"))
        self.btn_register.setText(_translate("launcherui", "注册"))
from qfluentwidgets import IndeterminateProgressBar, LineEdit, PushButton, SpinBox, SwitchButton
