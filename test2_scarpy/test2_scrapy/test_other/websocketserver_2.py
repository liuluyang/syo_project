from websocket_server import WebsocketServer


class ServerGate(object):
    def __init__(self):
        self.clients = list()
        print ('__int__')
        pass

    #当新的客户端连接时会提示
    # Called for every client connecting (after handshake)
    def new_client(self,client, server):
        print("新的连接 %d" % client['id'])
        server.send_message(client, "连接成功")
        self.clients.append(client)
        print (client)
        print('共%s个连接'%(len(self.clients)))

    # 当旧的客户端离开
    # Called for every client disconnecting
    def client_left(self,client, server):
        print("客户端(%d) 离开" % client['id'])
        self.clients.remove(client)
        print('共%s个连接' % (len(self.clients)))


    # 接收客户端的信息。
    # Called when a client sends a message
    def message_received(self,client, server, message):
        # if len(message) > 200:
        #     message = message[:200] + '..'
        print("客户端(%d) 信息: %s" % (client['id'], message))
        if message=='requset 1':
            server.send_message(client,'请求1')
        else:
            server.send_message(client,'请求2')

s = ServerGate()
PORT = 9001
server = WebsocketServer(PORT, "0.0.0.0")
server.set_fn_new_client(s.new_client)
server.set_fn_client_left(s.client_left)
server.set_fn_message_received(s.message_received)
server.run_forever()


