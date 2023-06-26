import json
import logging
import os
import socket
import time
from threading import Thread

import pymysql

# 数据库信息
DATABASE = {
    "address": "127.0.0.1",
    "port": 3306,
    "user": "minichat",
    "password": "MiniDB",
    "dbname": "minichat",
}
SERVER = {"bind": "0.0.0.0", "port": 9898}

conns = []

# 尝试启用日志系统
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    # 创建 handler 输出到文件
    file_handler = logging.FileHandler(
        "logs/" + str(round(time.time())) + ".log", mode="w", encoding="utf-8"
    )  # 一定要加上 mode='w'
    file_handler.setLevel(logging.DEBUG)
    qt_handler = logging.Handler()
    # handler 输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # 创建 logging format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(funcName)s:%(lineno)d] [%(name)s/%(levelname)s] : %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.info("日志系统上线!")
except Exception as e:
    print(e)
    print("日志系统启动失败")


# 初始化数据库
def InitDb():
    try:
        # 尝试连接
        log.info("尝试连接到数据库（{}:{}）".format(DATABASE["address"], DATABASE["port"]))
        db = pymysql.connect(
            host=DATABASE["address"],
            user=DATABASE["user"],
            passwd=DATABASE["password"],
            port=DATABASE["port"],
            db=DATABASE["dbname"],
        )
        log.info("成功连接到数据库！")
    except:
        log.critical("----------CRITICAL----------")
        log.critical("连接到数据库失败！！！", exc_info=True)
        log.critical("程序正在退出......")
        log.critical("----------CRITICAL----------")
        exit()
    log.debug("创建游标对象")
    cursor = db.cursor()
    try:
        # 初始化用户表
        log.debug("尝试建表：users")
        sql = """
        CREATE TABLE `users`  (
        `uuid` int NOT NULL,
        `nickname` varchar(255) NOT NULL,
        `avatar_id` int NOT NULL,
        `sex` int NOT NULL,
        `password` varchar(255) NOT NULL,
        `loginname` varchar(255) NOT NULL
        );
        """
        cursor.execute(sql)
        log.debug("新建的表：users")
    except Exception as e:
        if "1050" in str(e):
            log.debug("表：users 已存在")
        else:
            log.error("建表失败！", exc_info=True)

    try:
        # 初始化好友列表
        log.debug("尝试建表：friends")
        sql = """
        CREATE TABLE `friends`  (
        `uuid` int NOT NULL,
        `friend_id` int NOT NULL
        );
        """
        cursor.execute(sql)
        log.debug("新建的表：friends")
    except Exception as e:
        if "1050" in str(e):
            log.debug("表：friends 已存在")
        else:
            log.error("建表失败！", exc_info=True)

    try:
        # 初始化聊天列表
        log.debug("尝试建表： chats")
        sql = """
        CREATE TABLE `chats`  (
        `uuid` int NOT NULL,
        `friend_id` int NOT NULL,
        `chat_id` int NOT NULL
        );
        """
        cursor.execute(sql)
        log.debug("新建的表：chats")
    except Exception as e:
        if "1050" in str(e):
            log.debug("表：chats 已存在")
        else:
            log.error("建表失败！", exc_info=True)

    try:
        # 初始化私聊消息列表
        log.debug("尝试建表： chatmessages")
        sql = """
        CREATE TABLE `chatmessages`  (
        `uuid` int NOT NULL,
        `chat_id` int NOT NULL,
        `message` longtext,
        `file_id` int,
        `photo_id` int
        );
        """
        cursor.execute(sql)
        log.debug("新建的表：chatmessages")
    except Exception as e:
        if "1050" in str(e):
            log.debug("表：chatmessages 已存在")
        else:
            log.error("建表失败！", exc_info=True)


def CmdHandle():
    log.info("命令系统上线")
    try:
        while True:
            cmd = input("> ")
            if cmd == '':
                continue
    except Exception as e:
        log.error("命令系统出现错误，请重启服务器！", exc_info=True)


# 创建socket对象
def InitSvr():
    sock = socket.socket()
    try:
        # 尝试绑定服务器
        sock.bind((SERVER["bind"], SERVER["port"]))
        sock.listen(1000)
        log.info("服务器运行在地址（{}:{}）".format(SERVER["bind"], SERVER["port"]))
    except Exception as e:
        exc = str(e)
        log.critical("----------CRITICAL----------")
        log.critical(
            "无法绑定服务器到地址（{}:{}）！！".format(SERVER["bind"], SERVER["port"]), exc_info=True
        )
        log.critical("程序正在退出！")
        log.critical("----------CRITICAL----------")
        exit()
    tcmd = Thread(target=CmdHandle)
    tcmd.start()
    while True:
        s, addr = sock.accept()
        log.info("传入连接：{}".format(str(addr)))
        tmsg = Thread(target=MsgHandle, kwargs={'s': s, 'addr': addr})
        tmsg.start()


# 消息处理
def MsgHandle(s, addr):
    while True:
        try:
            # 接受消息
            msg = json.loads(s.recv(10240000).decode('utf-8'))
            log.info('客户端{}发送了一条消息：{}'.format(str(addr), msg))
            #time.sleep(0.1)
            #s.send('KEEP ALIVE'.encode('utf-8'))
        except Exception:
            log.error('一个客户端断开连接！{}'.format(str(addr)), exc_info=True)
            return
        if msg['cmd'] == 'test':
            log.info('客户端{}发送了服务器验证消息，正在答复'.format(str(addr)))
            s.send('{"cmd":"test", "status":"OK"}'.encode('utf-8'))


if __name__ == "__main__":
    InitDb()
    InitSvr()
