
from websocket import create_connection
import time
import json

#ws = create_connection('ws://127.0.0.1:9001/v1/market/')
#ws = create_connection('ws://203.195.153.53/v1/market/')
#ws = create_connection('ws://47.52.115.31/v1/market/')
#ws = create_connection('ws://47.75.223.85:9001/v1/market/')
ws_list = []
for i in range(1):
    ws_list.append(create_connection('ws://47.52.115.31/v1/market/'))
d = {'market':'gateio','method':'kline','symbol':'EOS_USDT','params':{'num':2, 'period':3600*24},'id':1}
#d = {'market':'binance','method':'trade','symbol':'PAX_BTC','params':{'num':500},'id':1}
d = json.dumps(d)
#time.sleep(70)


def data_parse(data):
    for num,d in enumerate(data):
        #if d['amount'] in [500000, 1000000]:
            print(num, time.localtime(d['time']), d)

while True:
    for num, ws in enumerate(ws_list):
        ws.send(d)
        data_recv = ws.recv()
        #print (num, type(data_recv), data_recv)
        data = json.loads(data_recv)
        #print (num,data['data'])
        for i in data['data']:
            print(i)
        #data_parse(data['data'])
        time.sleep(0.2)
        #ws.close()
    #time.sleep(5)