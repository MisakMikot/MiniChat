# coding:utf-8
import subprocess
import sys
import socket
import os
import json
import tkinter as tk
import tkinter.messagebox

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget, QMessageBox

from qfluentwidgets import (NavigationBar, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, SearchLineEdit, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar
from PyQt5 import QtCore, QtWidgets
from qfluentwidgets import LineEdit, PixmapLabel, PrimaryPushButton, PushButton, StrongBodyLabel, SubtitleLabel, Dialog

sid = ''
addr = ''
port = ''

# 初始化Tkinter
root = tk.Tk()
root.withdraw()


# 初始化连接并返回socket对象
def initClient():
    # 从文件读取SID，地址，端口
    try:
        with open('%s\\session.id' % os.path.split(os.path.realpath(__file__))[0], 'r') as f:
            sid = f.readline().replace(' ', '').replace('\n', '')
            addr = f.readline().replace(' ', '').replace('\n', '')
            port = int(f.readline().replace(' ', '').replace('\n', '')) + 1
            if sid == '' or addr == '' or port == '':
                raise
        os.remove('%s\\session.id' % os.path.split(os.path.realpath(__file__))[0])
    except Exception as e:
        tkinter.messagebox.showerror('错误', '无法正确获取会话ID，请使用启动器重新登录！')
        sys.exit()
    # 连接到服务器
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
    except Exception as e:
        tkinter.messagebox.showerror('错误', '无法连接到服务器')
        sys.exit()
    # 发送会话ID并等待验证
    try:
        s.send(json.dumps({'cmd':'verify_client', 'session_id': sid}).encode('utf-8'))
        msg = json.loads(s.recv(1024).decode('utf-8'))
        if not msg['cmd'] == 'verify_client':
            raise
        if not msg['status'] == 'success':
            raise
        return s
    except Exception as e:
        tkinter.messagebox.showerror('错误', '身份验证失败，')
        sys.exit()


class myInfo(QWidget):
    def __init__(self, s):
        super().__init__()
        self.s = s
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(568, 456)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.plabel_avatar = PixmapLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plabel_avatar.sizePolicy().hasHeightForWidth())
        self.plabel_avatar.setSizePolicy(sizePolicy)
        self.plabel_avatar.setObjectName("plabel_avatar")
        self.horizontalLayout.addWidget(self.plabel_avatar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_nickname = SubtitleLabel(Form)
        self.label_nickname.setText("")
        self.label_nickname.setAlignment(QtCore.Qt.AlignCenter)
        self.label_nickname.setObjectName("label_nickname")
        self.verticalLayout.addWidget(self.label_nickname)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_changeAvatar = PushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_changeAvatar.sizePolicy().hasHeightForWidth())
        self.btn_changeAvatar.setSizePolicy(sizePolicy)
        self.btn_changeAvatar.setObjectName("btn_changeAvatar")
        self.horizontalLayout_2.addWidget(self.btn_changeAvatar)
        self.btn_changeNickname = PushButton(Form)
        self.btn_changeNickname.setObjectName("btn_changeNickname")
        self.horizontalLayout_2.addWidget(self.btn_changeNickname)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(Form)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.horizontalLayout_3.addWidget(self.StrongBodyLabel)
        self.ledit_sex = LineEdit(Form)
        self.ledit_sex.setText("")
        self.ledit_sex.setReadOnly(True)
        self.ledit_sex.setObjectName("ledit_sex")
        self.horizontalLayout_3.addWidget(self.ledit_sex)
        self.btn_changeSex = PushButton(Form)
        self.btn_changeSex.setObjectName("btn_changeSex")
        self.horizontalLayout_3.addWidget(self.btn_changeSex)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.StrongBodyLabel_2 = StrongBodyLabel(Form)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.horizontalLayout_4.addWidget(self.StrongBodyLabel_2)
        self.ledit_birthday = LineEdit(Form)
        self.ledit_birthday.setObjectName("ledit_birthday")
        self.horizontalLayout_4.addWidget(self.ledit_birthday)
        self.btn_changeBirthday = PushButton(Form)
        self.btn_changeBirthday.setObjectName("btn_changeBirthday")
        self.horizontalLayout_4.addWidget(self.btn_changeBirthday)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.StrongBodyLabel_3 = StrongBodyLabel(Form)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.horizontalLayout_5.addWidget(self.StrongBodyLabel_3)
        self.ledit_loginname = LineEdit(Form)
        self.ledit_loginname.setObjectName("ledit_loginname")
        self.horizontalLayout_5.addWidget(self.ledit_loginname)
        self.btn_changeLoginname = PushButton(Form)
        self.btn_changeLoginname.setObjectName("btn_changeLoginname")
        self.horizontalLayout_5.addWidget(self.btn_changeLoginname)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_changePassword = PrimaryPushButton(Form)
        self.btn_changePassword.setProperty("hasIcon", False)
        self.btn_changePassword.setObjectName("btn_changePassword")
        self.horizontalLayout_6.addWidget(self.btn_changePassword)
        self.btn_quitLogin = PrimaryPushButton(Form)
        self.btn_quitLogin.setObjectName("btn_quitLogin")
        self.horizontalLayout_6.addWidget(self.btn_quitLogin)
        self.btn_deleteAccount = PrimaryPushButton(Form)
        self.btn_deleteAccount.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                             "    color: black;\n"
                                             "    background: rgba(255, 0, 0, 0.7);\n"
                                             "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                             "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                             "    border-radius: 5px;\n"
                                             "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                             "    padding: 5px 12px 6px 12px;\n"
                                             "    outline: none;\n"
                                             "}\n"
                                             "\n"
                                             "ToolButton {\n"
                                             "    padding: 5px 9px 6px 8px;\n"
                                             "}\n"
                                             "\n"
                                             "PushButton[hasIcon=false] {\n"
                                             "    padding: 5px 12px 6px 12px;\n"
                                             "}\n"
                                             "\n"
                                             "PushButton[hasIcon=true] {\n"
                                             "    padding: 5px 12px 6px 36px;\n"
                                             "}\n"
                                             "\n"
                                             "DropDownToolButton, PrimaryDropDownToolButton {\n"
                                             "    padding: 5px 31px 6px 8px;\n"
                                             "}\n"
                                             "\n"
                                             "DropDownPushButton[hasIcon=false],\n"
                                             "PrimaryDropDownPushButton[hasIcon=false] {\n"
                                             "    padding: 5px 31px 6px 12px;\n"
                                             "}\n"
                                             "\n"
                                             "DropDownPushButton[hasIcon=true],\n"
                                             "PrimaryDropDownPushButton[hasIcon=true] {\n"
                                             "    padding: 5px 31px 6px 36px;\n"
                                             "}\n"
                                             "\n"
                                             "PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
                                             "    background: rgba(255, 0, 0, 0.5);\n"
                                             "}\n"
                                             "\n"
                                             "PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
                                             "    color: rgba(0, 0, 0, 0.63);\n"
                                             "    background: rgba(249, 249, 249, 0.3);\n"
                                             "    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
                                             "}\n"
                                             "\n"
                                             "PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
                                             "    color: rgba(0, 0, 0, 0.36);\n"
                                             "    background: rgba(249, 249, 249, 0.3);\n"
                                             "    border: 1px solid rgba(0, 0, 0, 0.06);\n"
                                             "    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
                                             "}\n"
                                             "\n"
                                             "\n"
                                             "PrimaryPushButton,\n"
                                             "PrimaryToolButton,\n"
                                             "ToggleButton:checked,\n"
                                             "ToggleToolButton:checked {\n"
                                             "    color: white;\n"
                                             "    background-color: #ff0000;\n"
                                             "    border: 1px solid #ff0000;\n"
                                             "    border-bottom: 1px solid #007780;\n"
                                             "}\n"
                                             "\n"
                                             "PrimaryPushButton:hover,\n"
                                             "PrimaryToolButton:hover,\n"
                                             "ToggleButton:checked:hover,\n"
                                             "ToggleToolButton:checked:hover {\n"
                                             "    background-color: #ff0000;\n"
                                             "    border: 1px solid #ff0000;\n"
                                             "    border-bottom: 1px solid #007780;\n"
                                             "}\n"
                                             "\n"
                                             "PrimaryPushButton:pressed,\n"
                                             "PrimaryToolButton:pressed,\n"
                                             "ToggleButton:checked:pressed,\n"
                                             "ToggleToolButton:checked:pressed {\n"
                                             "    color: rgba(255, 255, 255, 0.63);\n"
                                             "    background-color: #ff0000;\n"
                                             "    border: 1px solid #ff0000;\n"
                                             "}\n"
                                             "\n"
                                             "PrimaryPushButton:disabled,\n"
                                             "PrimaryToolButton:disabled,\n"
                                             "ToggleButton:checked:disabled,\n"
                                             "ToggleToolButton:checked:disabled {\n"
                                             "    color: rgba(255, 255, 255, 0.9);\n"
                                             "    background-color: rgb(205, 205, 205);\n"
                                             "    border: 1px solid rgb(205, 205, 205);\n"
                                             "}\n"
                                             "\n"
                                             "SplitDropButton,\n"
                                             "PrimarySplitDropButton {\n"
                                             "    border-left: none;\n"
                                             "    border-top-left-radius: 0;\n"
                                             "    border-bottom-left-radius: 0;\n"
                                             "}\n"
                                             "\n"
                                             "#splitPushButton,\n"
                                             "#splitToolButton,\n"
                                             "#primarySplitPushButton,\n"
                                             "#primarySplitToolButton {\n"
                                             "    border-top-right-radius: 0;\n"
                                             "    border-bottom-right-radius: 0;\n"
                                             "}\n"
                                             "\n"
                                             "#splitPushButton:pressed,\n"
                                             "#splitToolButton:pressed,\n"
                                             "SplitDropButton:pressed {\n"
                                             "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                             "}\n"
                                             "\n"
                                             "PrimarySplitDropButton:pressed {\n"
                                             "    border-bottom: 1px solid #007780;\n"
                                             "}\n"
                                             "\n"
                                             "#primarySplitPushButton, #primarySplitToolButton {\n"
                                             "    border-right: 1px solid #3eabb3;\n"
                                             "}\n"
                                             "\n"
                                             "#primarySplitPushButton:pressed, #primarySplitToolButton:pressed {\n"
                                             "    border-bottom: 1px solid #007780;\n"
                                             "}\n"
                                             "\n"
                                             "HyperlinkButton {\n"
                                             "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                             "    padding: 6px 12px 6px 12px;\n"
                                             "    color: #009faa;\n"
                                             "    border: none;\n"
                                             "    border-radius: 6px;\n"
                                             "    background-color: transparent;\n"
                                             "}\n"
                                             "\n"
                                             "HyperlinkButton:hover {\n"
                                             "    background-color: rgba(0, 0, 0, 15);\n"
                                             "}\n"
                                             "\n"
                                             "HyperlinkButton:pressed {\n"
                                             "    background-color: rgba(0, 0, 0, 7);\n"
                                             "}\n"
                                             "\n"
                                             "HyperlinkButton:disabled {\n"
                                             "    color: rgba(0, 0, 0, 0.43)\n"
                                             "}\n"
                                             "\n"
                                             "\n"
                                             "RadioButton {\n"
                                             "    min-height: 24px;\n"
                                             "    max-height: 24px;\n"
                                             "    background-color: transparent;\n"
                                             "    font: 14px \'Segoe UI\', \'Microsoft YaHei\';\n"
                                             "    color: black;\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator {\n"
                                             "    width: 18px;\n"
                                             "    height: 18px;\n"
                                             "    border-radius: 11px;\n"
                                             "    border: 2px solid #999999;\n"
                                             "    background-color: rgba(0, 0, 0, 5);\n"
                                             "    margin-right: 4px;\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:hover {\n"
                                             "    background-color: rgba(0, 0, 0, 0);\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:pressed {\n"
                                             "    border: 2px solid #bbbbbb;\n"
                                             "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                             "            stop:0 rgb(255, 255, 255),\n"
                                             "            stop:0.5 rgb(255, 255, 255),\n"
                                             "            stop:0.6 rgb(225, 224, 223),\n"
                                             "            stop:1 rgb(225, 224, 223));\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:checked {\n"
                                             "    height: 22px;\n"
                                             "    width: 22px;\n"
                                             "    border: none;\n"
                                             "    border-radius: 11px;\n"
                                             "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                             "            stop:0 rgb(255, 255, 255),\n"
                                             "            stop:0.5 rgb(255, 255, 255),\n"
                                             "            stop:0.6 #009faa,\n"
                                             "            stop:1 #009faa);\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:checked:hover {\n"
                                             "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                             "            stop:0 rgb(255, 255, 255),\n"
                                             "            stop:0.6 rgb(255, 255, 255),\n"
                                             "            stop:0.7 #009faa,\n"
                                             "            stop:1 #009faa);\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:checked:pressed {\n"
                                             "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                             "            stop:0 rgb(255, 255, 255),\n"
                                             "            stop:0.5 rgb(255, 255, 255),\n"
                                             "            stop:0.6 #009faa,\n"
                                             "            stop:1 #009faa);\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton:disabled {\n"
                                             "    color: rgba(0, 0, 0, 110);\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:disabled {\n"
                                             "    border: 2px solid #bbbbbb;\n"
                                             "    background-color: transparent;\n"
                                             "}\n"
                                             "\n"
                                             "RadioButton::indicator:disabled:checked {\n"
                                             "    border: none;\n"
                                             "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                             "            stop:0 rgb(255, 255, 255),\n"
                                             "            stop:0.5 rgb(255, 255, 255),\n"
                                             "            stop:0.6 rgba(0, 0, 0, 0.2169),\n"
                                             "            stop:1 rgba(0, 0, 0, 0.2169));\n"
                                             "}\n"
                                             "\n"
                                             "TransparentToolButton,\n"
                                             "TransparentToggleToolButton,\n"
                                             "TransparentDropDownToolButton,\n"
                                             "TransparentPushButton,\n"
                                             "TransparentDropDownPushButton,\n"
                                             "TransparentTogglePushButton {\n"
                                             "    background-color: transparent;\n"
                                             "    border: none;\n"
                                             "    border-radius: 5px;\n"
                                             "    margin: 0;\n"
                                             "}\n"
                                             "\n"
                                             "TransparentToolButton:hover,\n"
                                             "TransparentToggleToolButton:hover,\n"
                                             "TransparentDropDownToolButton:hover,\n"
                                             "TransparentPushButton:hover,\n"
                                             "TransparentDropDownPushButton:hover,\n"
                                             "TransparentTogglePushButton:hover {\n"
                                             "    background-color: rgba(0, 0, 0, 9);\n"
                                             "    border: none;\n"
                                             "}\n"
                                             "\n"
                                             "TransparentToolButton:pressed,\n"
                                             "TransparentToggleToolButton:pressed,\n"
                                             "TransparentDropDownToolButton:pressed,\n"
                                             "TransparentPushButton:pressed,\n"
                                             "TransparentDropDownPushButton:pressed,\n"
                                             "TransparentTogglePushButton:pressed {\n"
                                             "    background-color: rgba(0, 0, 0, 6);\n"
                                             "    border: none;\n"
                                             "}\n"
                                             "\n"
                                             "TransparentToolButton:disabled,\n"
                                             "TransparentToggleToolButton:disabled,\n"
                                             "TransparentDropDownToolButton:disabled,\n"
                                             "TransprentPushButton:disabled,\n"
                                             "TransparentDropDownPushButton:disabled,\n"
                                             "TransprentTogglePushButton:disabled {\n"
                                             "    background-color: transparent;\n"
                                             "    border: none;\n"
                                             "}\n"
                                             "")
        self.btn_deleteAccount.setObjectName("btn_deleteAccount")
        self.horizontalLayout_6.addWidget(self.btn_deleteAccount)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_changeAvatar.setText(_translate("Form", "修改头像"))
        self.btn_changeNickname.setText(_translate("Form", "修改昵称"))
        self.StrongBodyLabel.setText(_translate("Form", "性别："))
        self.btn_changeSex.setText(_translate("Form", "修改"))
        self.StrongBodyLabel_2.setText(_translate("Form", "生日："))
        self.btn_changeBirthday.setText(_translate("Form", "修改"))
        self.StrongBodyLabel_3.setText(_translate("Form", "登录名："))
        self.btn_changeLoginname.setText(_translate("Form", "修改"))
        self.btn_changePassword.setText(_translate("Form", "修改密码"))
        self.btn_quitLogin.setText(_translate("Form", "退出登录"))
        self.btn_deleteAccount.setText(_translate("Form", "删除账号"))


class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        # add search line edit
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText('搜索应用、游戏、电影、设备等')
        self.searchLineEdit.setFixedWidth(400)
        self.searchLineEdit.setClearButtonEnabled(True)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        self.searchLineEdit.move((self.width() - self.searchLineEdit.width()) // 2, 8)


class Window(FramelessWindow):

    def __init__(self,s):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        # create sub interface
        # self.homeInterface = Widget('Home Interface', self)
        # self.appInterface = Widget('Application Interface', self)
        # self.videoInterface = Widget('Video Interface', self)
        self.myInfoInterface = QtWidgets.QWidget()
        self.myinfo = myInfo(s)
        self.myinfo.setupUi(self.myInfoInterface)
        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def closeEvent(self, event):
        # 重写关闭事件
        w = Dialog('信息', '是否要退出MiniChat登录器')
        if w.exec():
            pid = os.getpid()
            _ = subprocess.Popen('taskkill /F /PID %s' % str(pid))
        else:
            event.ignore()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        # self.addSubInterface(self.homeInterface, FIF.HOME, '主页', selectedIcon=FIF.HOME_FILL)
        # self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        # self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频')

        self.addSubInterface(self.myInfoInterface, FIF.BOOK_SHELF, '我', NavigationItemPosition.BOTTOM,
                             FIF.LIBRARY_FILL)
        self.navigationBar.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        # self.navigationBar.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = Window(initClient())
    w.show()
    app.exec_()
