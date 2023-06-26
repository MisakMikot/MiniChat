import json
import logging
import os
import socket
import subprocess
import time
import uuid
from threading import Thread

import pymysql

# 数据库信息
DATABASE = {
    "address": "127.0.0.1",
    "port": 3306,
    "user": "minichat",
    "password": "MiniDB",
    "dbname": "minichat",
    "autocommit": False
}
SERVER = {"bind": "0.0.0.0", "port": 9898}
commands = [{"cmd": "stop", "needParams": False,
             "operation": "log.info('正在关闭服务器');cursor.execute('drop table sessions'); db.close(); pid = os.getpid(); subprocess.Popen('taskkill /F /PID {}'.format(pid));"}]

conns = []
db = None
cursor = None

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

___aaa = subprocess.PIPE


# 初始化数据库
def InitDb():
    global db
    global cursor
    try:
        # 尝试连接
        log.info("尝试连接到数据库（{}:{}）".format(DATABASE["address"], DATABASE["port"]))
        db = pymysql.connect(
            host=DATABASE["address"],
            user=DATABASE["user"],
            passwd=DATABASE["password"],
            port=DATABASE["port"],
            db=DATABASE["dbname"],
            autocommit=DATABASE['autocommit']
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
        `uuid` int NOT NULL AUTO_INCREMENT,
        `nickname` varchar(255) NOT NULL,
        `avatar_id` int NOT NULL,
        `sex` int NOT NULL,
        `password` varchar(255) NOT NULL,
        `loginname` varchar(255) NOT NULL,
        `birth_year` int(4) NOT NULL,
        `birth_month` int(2) NOT NULL,
        `birth_day` int(2) NOT NULL,
        PRIMARY KEY (`uuid`)
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
        # 初始化会话表
        log.debug("尝试建表：sessions")
        sql = """
        CREATE TABLE `minichat`.`sessions`  (
            `sessionID` varchar(255) NOT NULL,
            `uuid` int NOT NULL
            );
            """
        cursor.execute(sql)
        log.debug("新建的表：sessions")
    except Exception as e:
        if "1050" in str(e):
            log.debug("表：sessions 已存在")
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


# 命令系统
def CmdHandle():
    # 命令列表
    log.info("命令系统上线")
    try:
        while True:
            # 获取输入
            isCommand = 0
            cmd = input("> ")
            if cmd == '':
                continue
            cmds = cmd.split(' ')
            # 分离命令和参数
            maincmd = cmds[0]
            for i in commands:
                if not maincmd == i["cmd"]:
                    continue
                if i['needParams']:
                    try:
                        # 带有参数的命令
                        param = cmd[1]
                        command = i['operation'].replace('#PARAM#', param)
                        log.info('执行命令“%s”，传入参数“%s”' % (maincmd, param))
                        exec(command)
                        break
                    except IndexError:
                        log.error('命令“%s”需要有效的参数输入' % maincmd)
                        break
                    except:
                        log.error('命令“%s”在执行过程中出现了错误' % cmd, exc_info=True)
                else:
                    # 正常命令
                    command = i['operation']
                    try:
                        exec(command)
                    except:
                        log.error('命令“%s”在执行过程中出现了错误' % cmd, exc_info=True)
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


def genName():
    id = 'MC老哥_' + str(uuid.uuid4()).split('-')[1]
    return id


# 生成会话ID并验证
def genSessionID():
    while True:
        sid = str(uuid.uuid4()).replace('-', '')
        sql = 'SELECT * FROM `sessions` WHERE sessionID="%s"' % sid
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            continue
        else:
            return sid


# 消息处理
def MsgHandle(s, addr):
    while True:
        try:
            # 接受消息
            raw = s.recv(10240000).decode('utf-8')
            print(raw)
            msg = json.loads(raw)
            log.info('客户端{}发送了一条消息：{}'.format(str(addr), raw))
            # time.sleep(0.1)
            # s.send('KEEP ALIVE'.encode('utf-8'))
        except Exception:
            log.error('一个客户端断开连接！{}'.format(str(addr)), exc_info=True)
            return
        # 验证服务器答复
        if msg['cmd'] == 'test':
            log.info('客户端{}发送了服务器验证消息，正在答复'.format(str(addr)))
            s.send(json.dumps({"cmd": "test", "status": "OK"}).encode('utf-8'))
        # 检查用户名可用性
        elif msg['cmd'] == 'check_username':
            username = msg['username']
            log.info('客户端{}请求验证用户名“{}”是否合法，正在查询...'.format(str(addr), username))
            sql = "SELECT * FROM users WHERE loginname='{}'".format(username)
            cursor.execute(sql)
            results = cursor.fetchall()
            names = len(results)
            if not names == 0:
                log.debug(str(results))
                log.info('对于客户端{}发送的用户名可用性检查请求，查询到有匹配的用户名，向客户端发送错误信息...'.format(
                    str(addr)))
                s.send(json.dumps({"cmd": "check_username", "status": "existed"}).encode('utf-8'))
            else:
                log.info('对于客户端{}发送的用户名可用性检查请求，没有查询到匹配的用户名，向客户端发送结果...'.format(
                    str(addr)))
                s.send(json.dumps({"cmd": "check_username", "status": "ok"}).encode('utf-8'))
        # 添加注册信息
        elif msg['cmd'] == 'register':
            username = msg['username']
            password = msg['password']
            log.info('用户名{}被客户端{}请求注册，正在向数据库添加信息...'.format(username, str(addr)))
            sql = "INSERT INTO users (nickname,  \
                  avatar_id, sex, password, loginname,  \
                  birth_year, birth_month, birth_day)  \
                  VALUES ('%s', %s, %s, '%s', '%s', %s, %s, %s)" % \
                  (genName(), 0, 0, password, username, 2000, 1, 1)
            try:
                cursor.execute(sql)
                db.commit()
                log.info('向数据库添加了一条记录')
                s.send(json.dumps({"cmd": "register", "status": "ok"}).encode())
            except Exception as e:
                log.error('发生错误，正在回滚数据库', exc_info=True)
                db.rollback()
                s.send(json.dumps({"cmd": "register", "status": "error", "errmsg": str(e)}).encode())
        # 获取会话代码
        elif msg['cmd'] == 'get_session_code':
            username = msg['username']
            password = msg['password']
            log.info('客户端%s请求用户“%s”的会话代码，正在查询..' % (str(addr), username))
            # 验证账号密码是否正确
            sql = 'SELECT * FROM `users` WHERE loginname="%s" AND `password`="%s"' % (username, password)
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            if not result:
                log.warning('客户端%s请求了错误的用户名或密码，返回错误信息' % str(addr))
                s.send(json.dumps({"cmd": "get_session_code", "status": "wrong"}).encode('utf-8'))
            else:
                log.info('生成会话代码并将查询结果发送至客户端%s' % str(addr))
                sid = genSessionID()
                uid = result[0]
                nickname = result[1]
                sql = """INSERT INTO sessions ( sessionID, uuid )
                            VALUES
                                (%s, %s)
                """ % (sid, uid)
                s.send(json.dumps({"cmd": "get_session_code", "status": "ok", "code": sid, "nickname": nickname}).encode('utf-8'))


if __name__ == "__main__":
    InitDb()
    InitSvr()
