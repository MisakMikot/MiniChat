import json
import logging
import os
import socket
import subprocess
import sys
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
    "autocommit": False
}
# 端口为登录服务器+1
SERVER = {"bind": "0.0.0.0", "port": 9899}
# 预设指令
commands = [{"cmd": "stop", "needParams": False,
             "operation": "log.info('正在关闭服务器');cursor.execute('drop table sessions'); db.close(); pid = os.getpid(); subprocess.Popen('taskkill /F /PID {}'.format(pid));"}]
_useless = subprocess.PIPE

# 尝试启用日志系统
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    # 创建 handler 输出到文件
    file_handler = logging.FileHandler(
        "logs/" + "chat_" + str(round(time.time())) + ".log", mode="w", encoding="utf-8"
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
    sys.exit()

# 连接数据库
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


# 验证会话ID
def verifySessionId(sid):
    sql = 'SELECT * FROM `sessions` WHERE sessionID="%s"' % sid
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        return False
    else:
        return True


# 从会话ID获取UUID
def session_id_to_uuid(sid):
    sql = 'SELECT * FROM `sessions` WHERE sessionID="%s"' % sid
    cursor.execute(sql)
    results = cursor.fetchone()
    if not results:
        return False
    else:
        return results[1]


def MsgHandle(s, addr):
    # 验证客户端
    authed = False
    session_id = ''
    def verifyClient():
        time.sleep(3)
        if not authed:
            log.info('客户端%s未通过验证' % str(addr))
            s.close()
            return
    tVerifyClient = Thread(target=verifyClient)
    tVerifyClient.start()
    while True:
        try:
            # 接受消息
            raw = s.recv(10240000).decode('utf-8')
            msg = json.loads(raw)
            log.info('客户端{}发送了一条消息：{}'.format(str(addr), raw))
        except json.decoder.JSONDecodeError:
            log.error('解析客户端%s发送的信息时错误，可能是遇到了网络粘包问题' % str(addr), exc_info=True)
            continue
        except Exception:
            log.error('一个客户端断开连接！{}'.format(str(addr)), exc_info=True)
            s.close()
            return
        try:
            # 处理信息
            # 验证会话ID
            if msg['cmd'] == 'verify_client':
                session_id = msg['session_id']
                if verifySessionId(session_id):
                    authed = True
                    s.send(json.dumps({'cmd': 'verify_client', 'status': 'success'}).encode('utf-8'))
                else:
                    s.send(json.dumps({'cmd': 'verify_client', 'status': 'failed'}).encode('utf-8'))
                    s.close()
        except IndexError:
            log.error('客户端%s发送了不合法信息' % str(addr), exc_info=True)


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


tcmd = Thread(target=CmdHandle)
tcmd.start()
