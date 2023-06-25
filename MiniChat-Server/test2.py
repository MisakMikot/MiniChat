import socket
import time
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    send_data = '111111111111111111111111111111111111'
    print(send_data)
    s.sendto(bytes(send_data,encoding = 'utf8'),('127.0.0.1',9999))    
    # 客户端接收来自服务器端发送的数据
    recv_data =  str(s.recv(1024),encoding='utf8')
    print(recv_data)  
    time.sleep(2)
s.close()