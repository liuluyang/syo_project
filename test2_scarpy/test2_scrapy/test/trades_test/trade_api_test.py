from websocket import create_connection
import time
import json

ws = create_connection('ws://47.75.223.85/v1/market/')
last_id = None
data_f = {'market':'huobi','method':'trade','symbol':'BTC_USDT','params':{},'id':1}

while True:
    if last_id:
        data_f['params'] = {'last_id':last_id}
    data_send = json.dumps(data_f)
    ws.send(data_send)
    data_recv = ws.recv()
    data = json.loads(data_recv)
    if data['error'] is None:
        data_list = data['data']
        if data_list:
            last_id = data_list[-1]['id']
        print (data)
    time.sleep(1)