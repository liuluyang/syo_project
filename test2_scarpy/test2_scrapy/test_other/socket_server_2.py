

import socket
import threading
import time
import random

ip_port = ('127.0.0.1',8080)
sock = socket.socket()
sock.bind(ip_port)
sock.listen(5)
#sock.settimeout(5)


def tcplink(conn, addr):
    conn.send('欢迎'.encode())
    while True:
        data_revice = conn.recv(1024).decode()
        if data_revice:
            print ('来自：%s, 内容：%s'%(addr, data_revice))
            data_send = '我是服务器'.encode()
            conn.send(data_send)
        if data_revice=='exit':
            print('来自：%s, 内容：%s' % (addr, data_revice))
            # data_send = '关闭当前连接。。。'.encode()
            # conn.send(data_send)
            break

    conn.close()
    print('关闭当前连接。。。')

def tcplink_2(conn, addr):
    conn.send('欢迎'.encode())
    while True:
        data_revice = conn.recv(1024).decode()
        if data_revice:
            print ('来自：%s, 内容：%s'%(addr, data_revice))
            data_send = '我是服务器'.encode()
            conn.send(data_send)
        if not data_revice:
            time.sleep(1)
            data_send = '定时发送'.encode()
            conn.send(data_send)
        if data_revice=='exit':
            print('来自：%s, 内容：%s' % (addr, data_revice))
            # data_send = '关闭当前连接。。。'.encode()
            # conn.send(data_send)
            break

    conn.close()
    print('关闭当前连接。。。')

def tcplink_3(conn, addr):
    conn.send('欢迎'.encode())
    while True:
        time.sleep(1)
        #data_revice = conn.recv(1024).decode()
        data_send = random.choice([1,2,3,4,5])
        if data_send == 1:
            data_send = str(data_send).encode()
            conn.send(data_send)
        # if data_revice=='exit':
        #     break

    # conn.close()
    # print('关闭当前连接。。。')

#多线程服务端测试
while True:
    print ('等待连接。。。')
    conn,addr = sock.accept()
    print ('有一个新的连接：',addr)

    t = threading.Thread(target=tcplink_3, args=(conn, addr))
    t.start()












