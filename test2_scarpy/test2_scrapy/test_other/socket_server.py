

import socket
import threading


ip_port = ('127.0.0.1',8080)
sock = socket.socket()
sock.bind(ip_port)
sock.listen(5)

#单线程服务端测试
while True:
    print ('等待连接。。。')
    conn,addr = sock.accept()

    while True:
        data_revice = conn.recv(1024).decode()

        if data_revice:
            print ('来自：%s, 内容：%s'%(addr, data_revice))
            data_send = '我是服务器'.encode()
            conn.send(data_send)

        if data_revice=='exit':
            print('来自：%s, 内容：%s' % (addr, data_revice))
            print('关闭当前连接。。。')
            # data_send = '关闭当前连接。。。'.encode()
            # conn.send(data_send)
            break








