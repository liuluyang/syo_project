
from websocket import create_connection
import time

#ws = create_connection('ws://127.0.0.1:9001')
ws_list = []
for i in range(1):
    ws_list.append(create_connection('ws://47.52.115.31/v1/kuaixun/'))
news_num = 0
while True:
    for num, ws in enumerate(ws_list):
        #ws.send(str(num))
        data = ws.recv()
        news_num+=int(data)
        print (news_num)
        #time.sleep(1)
        #pass