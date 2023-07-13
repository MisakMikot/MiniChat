import hashlib
import json
import os
import socket
import sys
import time
from threading import Thread
from subprocess import Popen

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication
from qfluentwidgets import InfoBar, InfoBarPosition, Dialog

from Ui_launcher import Ui_launcherui

s = socket.socket()
addr = ''
port=0
connected = False
trustedServer = False
availableUsername = 'waiting'
regStat = 'waiting'
logStat = 'waiting'

nickname = None
sid=None


class MyLauncher(QMainWindow):
    # 重写QMainWindow类
    def closeEvent(self, event):
        w = Dialog('信息', '是否要退出MiniChat登录器')
        if w.exec():
            s.close()
            pid = os.getpid()
            _ = Popen('taskkill /F /PID %s' % str(pid))
            # 通知服务器的代码省略，这里不是重点...
        else:
            event.ignore()


class slots(QObject):
    # 定义槽函数
    def error(self, title: str, content: str) -> None:
        # 显示错误信息
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,  # won't disappear automatically
            parent=lclass,
        )

    def loadon(self):
        # 显示加载条
        launcher.IndeterminateProgressBar.show()

    def loadoff(self):
        # 隐藏加载条
        launcher.IndeterminateProgressBar.hide()

    def info(self, title, content):
        # 显示错误信息
        InfoBar.info(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,  # won't disappear automatically
            parent=lclass,
        )

    def unlock(self):
        launcher.ledit_account.setDisabled(False)
        launcher.ledit_password.setDisabled(False)
        launcher.ledit_passwordre.setDisabled(False)
        launcher.btn_login.setDisabled(False)
        launcher.btn_register.setDisabled(False)
        launcher.swich_savelogin.setDisabled(False)
        launcher.ledit_addr.setDisabled(True)
        launcher.sbox_port.setDisabled(True)

    def lock(self):
        launcher.ledit_account.setDisabled(True)
        launcher.ledit_password.setDisabled(True)
        launcher.ledit_passwordre.setDisabled(True)
        launcher.btn_login.setDisabled(True)
        launcher.btn_register.setDisabled(True)
        launcher.swich_savelogin.setDisabled(True)
        launcher.ledit_addr.setDisabled(False)
        launcher.sbox_port.setDisabled(False)


# 定义信号
class ui(QObject):
    signal_error = pyqtSignal(str, str)
    signal_loadon = pyqtSignal()
    signal_loadoff = pyqtSignal()
    signal_info = pyqtSignal(str, str)
    signal_unlock = pyqtSignal()
    signal_lock = pyqtSignal()

    def __init__(self):
        super(ui, self).__init__()

    def error(self, title, content):
        # 显示错误信息
        self.signal_error.emit(title, content)

    def loadon(self):
        # 显示加载条
        self.signal_loadon.emit()

    def loadoff(self):
        # 隐藏加载条
        self.signal_loadoff.emit()

    def info(self, title, content):
        self.signal_info.emit(title, content)

    def lock(self):
        self.signal_lock.emit()

    def unlock(self):
        self.signal_unlock.emit()


def md5(message: str):
    encode1 = hashlib.new('md5', message.encode('utf-8')).hexdigest()
    encode2 = hashlib.new('md5', encode1.encode('utf-8')).hexdigest()
    result = hashlib.new('md5', encode2.encode('utf-8')).hexdigest()
    return result


# 处理消息
def msgHaldle(s):
    global trustedServer
    global availableUsername
    global regStat
    global logStat
    global nickname
    global sid
    trustedServer = False
    # 验证服务器是否为聊天服务器
    ui.info('信息', '正在验证服务器')
    ui.loadon()
    s.send('{"cmd":"test"}'.encode('utf-8'))

    # 验证超时检测
    def testTimer():
        time.sleep(5)
        if trustedServer:
            ui.info('信息', '这是受信任的MiniChat服务器')
            ui.loadoff()
            ui.unlock()
        else:
            ui.error('错误', '这不是受信任的MiniChat服务器')
            ui.loadoff()
            connect()

    t = Thread(target=testTimer)
    t.start()
    while True:
        # 接受消息
        try:
            msg = json.loads(s.recv(1024000).decode('utf-8'))
        except Exception as e:
            if '10038' in str(e) or '10053' in str(e) or '10054' in str(e):
                ui.info(title='信息', content='连接断开')
                connect()
                return
            else:
                ui.error(title='错误', content=str(e))
                return

        print(msg)
        # 服务器测试消息
        if msg["cmd"] == 'test' and msg["status"] == 'OK':
            trustedServer = True
        # 用户名检查结果
        if msg['cmd'] == 'check_username':
            if msg['status'] == 'existed':
                availableUsername = 'existed'
            elif msg['status'] == 'ok':
                availableUsername = 'ok'
        # 注册结果
        if msg['cmd'] == 'register':
            if msg['status'] == 'ok':
                regStat = 'ok'
            elif msg['status'] == 'error':
                regStat = 'error'
                errmsg = msg['errmsg']
                ui.error('注册失败', errmsg)
        # 登录结果
        if msg['cmd'] == 'get_session_code':
            if msg['status'] == 'ok':
                nickname = msg['nickname']
                logStat = 'ok'
                sid = msg['code']
            elif msg['status'] == 'wrong':
                logStat = 'wrong'
            elif msg['status'] == 'already_login':
                logStat = 'already_login'



# 连接按钮触发操作
def connect():
    global s
    global connected
    global addr
    global port
    if connected:
        # 断开连接
        s.close()
        launcher.btn_conn.setText('连接')
        connected = False
        s = socket.socket()
        ui.lock()
        return
    # 获取地址
    addr = launcher.ledit_addr.text()
    port = launcher.sbox_port.text()
    if addr == "":
        # 检查地址
        ui.error("错误", "服务器地址应该被填写")
        return
    ui.loadon()
    try:
        # 获取IP
        server_ip = socket.gethostbyname(addr)
    except Exception as e:
        ui.error(title="定位服务器失败", content=str(e))
        ui.loadoff()
        return
    try:
        # 连接服务器
        s.connect((server_ip, int(port)))
    except Exception as e:
        ui.error(title="连接服务器失败", content=str(e))
        ui.loadoff()
        return
    ui.loadoff()
    ui.info(title='信息', content='连接到服务器')
    launcher.btn_conn.setText('断开')
    connected = True
    t = Thread(target=msgHaldle, kwargs={'s': s})
    t.start()


# 注册账号
def register():
    global availableUsername
    global regStat
    # 获取用户名，密码，重复密码
    ui.loadon()
    account = launcher.ledit_account.text()
    password = launcher.ledit_password.text()
    passwordre = launcher.ledit_passwordre.text()
    # 判断是否为空
    if account == '' or password == '' or passwordre == '':
        ui.error('错误', '用户名或密码不能为空')
        ui.loadoff()
        return
    # 判断重复密码是否正确
    if not password == passwordre:
        ui.error('错误', '密码不符')
        ui.loadoff()
        return
    # 检查用户名是否被占用
    s.send(json.dumps({"cmd":"check_username", "username":account}).encode('utf-8'))
    while True:
        time.sleep(0.1)
        if availableUsername == 'waiting':
            continue
        if availableUsername == 'existed':
            availableUsername = 'waiting'
            ui.error('错误', '用户名已被占用')
            ui.loadoff()
            return
        else:
            break
    s.send(json.dumps({"cmd":"register", "username":account, "password":md5(password)}).encode('utf-8'))
    while True:
        time.sleep(0.1)
        if regStat == 'waiting':
            continue
        elif regStat == 'error':
            ui.loadoff()
            return
        elif regStat == 'ok':
            regStat = 'waiting'
            ui.info('信息', '注册成功，欢迎加入MiniChat')
            ui.loadoff()
            break


def startCli():
    pass


# 登录并获取会话代码
def login():
    # 获取输入
    global logStat
    ui.loadon()
    account = launcher.ledit_account.text()
    password = launcher.ledit_password.text()
    if account == '' or password == '':
        ui.error('错误', '账号或密码不能为空')
        ui.loadoff()
        return
    s.send(json.dumps({"cmd":"get_session_code", "username":account, "password":md5(password)}).encode('utf-8'))
    while True:
        # 检查登录状态
        time.sleep(0.1)
        if logStat == 'waiting':
            continue
        elif logStat == 'wrong':
            ui.error('错误', '用户名或密码错误')
            logStat = 'waiting'
            ui.loadoff()
        elif logStat == 'already_login':
            ui.error('错误', '该账号在另一台设备上登录')
            logStat = 'waiting'
            ui.loadoff()
        elif logStat == 'ok':
            ui.info('信息','登录成功，欢迎回来，%s' % nickname)
            logStat = 'waiting'
            with open('%s\\session.id' % os.path.split(os.path.realpath(__file__))[0], 'w') as f:
                # 写入会话代码
                f.write(sid+'\n'+addr+'\n'+str(port))
            time.sleep(0.1)
            startCli()
            ui.loadoff()
            s.close()
            pid = os.getpid()
            _ = Popen('taskkill /F /PID %s' % str(pid))


# 信号槽连接
def slotConn():
    launcher.btn_conn.clicked.connect(lambda: Thread(target=connect).start())
    launcher.btn_register.clicked.connect(lambda: Thread(target=register).start())
    launcher.btn_login.clicked.connect(lambda :Thread(target=login).start())
    # 自定义信号连接
    ui.signal_error.connect(slots.error)
    ui.signal_loadon.connect(slots.loadon)
    ui.signal_loadoff.connect(slots.loadoff)
    ui.signal_info.connect(slots.info)
    ui.signal_lock.connect(slots.lock)
    ui.signal_unlock.connect(slots.unlock)


# 程序主函数
def main():
    if not os.path.isdir("data"):
        # 检查数据目录
        os.mkdir("data")
    # if not os.path.isfile('data/login.data'):
    # 检查登录信息
    # with open('data/login.data'):
    # pass


if __name__ == "__main__":
    # 程序入口
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    lclass = MyLauncher()
    launcher = Ui_launcherui()
    launcher.setupUi(lclass)
    launcher.IndeterminateProgressBar.hide()
    launcher.ledit_account.setValidator(QRegExpValidator(QRegExp('[a-zA-Z0-9]+$')))
    ui = ui()
    slots = slots()
    slotConn()
    lclass.show()
    sys.exit(app.exec_())
