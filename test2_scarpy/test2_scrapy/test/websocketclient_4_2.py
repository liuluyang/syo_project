
from websocket import create_connection
import time
import json

#ws = create_connection('ws://127.0.0.1:9001/v1/market/')
#ws = create_connection('ws://203.195.153.53/v1/market/')
ws_list = []
for i in range(1):
    ws_list.append(create_connection('ws://192.168.1.111:9001/v1/market/kline/'))
#d = {'market':'gateio','method':'ticker','symbol':'AE_BTC','params':{},'id':1}
d = {'market':'gateio','method':'kline','symbol':'BTC_USDT','params':{'period':1800, 'num':100},'id':1}
d = json.dumps(d)
#time.sleep(70)
while True:
    for num, ws in enumerate(ws_list):
        ws.send(d)
        data_recv = ws.recv()
        #print (num, type(data_recv), data_recv)
        data = json.loads(data_recv)
        print (num,data)
        time.sleep(0.5)
        #ws.close()
    #time.sleep(5)