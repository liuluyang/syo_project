from websocket import create_connection
import time

ws_list = [create_connection('ws://203.195.153.53/uce/echo') for i in range(20)]

while True:
    for num,ws in enumerate(ws_list):
        ws.send(str(num))
        print (ws.recv())
        #ws.close()
        #print ('关闭')
        time.sleep(1)
# for i in range(10):
#     ws = create_connection('ws://203.195.153.53:9001/uce/echo')
#     ws.send('h')
#     print (ws.recv())
#     ws.close()