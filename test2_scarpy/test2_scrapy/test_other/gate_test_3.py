#from socket import create_connection
from websocket import create_connection
#from websocket2 import create_connection
import json
import time


# ws = create_connection("wss://ws.gateio.io/v3/")
# print (ws)
# data_send = '{"id":12309, "method":"trades.query", "params":["BTC_USDT", 1, 7938163]}'
# while True:
#     print (ws.getstatus)
#     time.sleep(80)
#     print ('ws')
#     print(ws.getstatus)
#     ws = create_connection("wss://ws.gateio.io/v3/")
#     print (ws.send(data_send))
#     print (ws.recv())



# ws = create_connection("wss://ws.gateio.io/v3/")
# print (ws)
ws_list = []
for i in range(10):
    ws_list.append(create_connection("wss://ws.gateio.io/v3/"))
data_send = '{"id":12312, "method":"ticker.query", "params":["BTC_USDT", 60]}'
while True:
    for num,ws in enumerate(ws_list):
        print (num)
        ws.send(data_send)
        print (ws.recv())
        #time.sleep(1)
