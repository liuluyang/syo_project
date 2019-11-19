
import socket

ip_port = ('127.0.0.1',8080)
sock = socket.socket()
sock.connect(ip_port)

while True:
    data_send = input('请输入：')
    data_send = data_send.encode()
    sock.send(data_send)
    revice = sock.recv(1024).decode()
    print ('服务器：',revice)
    if data_send=="exit".encode():
        print ('关闭连接')
        sock.close()
        break


