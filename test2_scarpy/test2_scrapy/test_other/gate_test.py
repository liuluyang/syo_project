#from socket import create_connection
from websocket import create_connection
#from websocket2 import create_connection
import json
import time


ws = create_connection("wss://ws.gateio.io/v3/")
print (ws)
#ws.send('{"id":12312, "method":"server.ping", "params":[]}')
#print(ws.recv())
# data_send = '{"id":1, "method":"kline.query", "params":' \
#             '["BTC_USDT", 1516950119, 1516951219, 1800]}'
# data_send = '{"id":12312, "method":"ticker.query", "params":["EOS_USDT", 86400]}'
data_send = '{"id":12309, "method":"trades.query", "params":["BTC_USDT", 1, 7938163]}'
num = 0
while True:
    #for i in range(1):
        # time_now = time.time()
        # time_befor = time_now-100
        # data_send = '{"id":1, "method":"kline.query", "params":' \
        #             '["BTC_USDT", %s, %s, 1800]}'%(int(time_befor),int(time_now))
        # print (data_send)
    ws.send(data_send)
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    print (data_recv['error'])
    if not data_recv['error']:
    #     print (len(data_recv['result']))
    #     print (data_recv['result'])
        for per in data_recv['result']:
            print (per)
    time.sleep(1)
    num+=1
    print (num)