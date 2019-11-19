from websocket import create_connection
import time, json, random


symbol = 'btcusdt'
data_send = {'event':'addChannel', 'channel':'{}_trades'.format(symbol)}
data_send = json.dumps(data_send)
ws = create_connection('wss://api.zb.cn:9999/websocket')
ws.send(data_send)

while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    data = data_recv['data']
    for d in data:
        is_buy = True if d['type'] == 'buy' else False
        if is_buy:
            print('买入：', d)
        else:
            print('卖出：', d)
    print('__________________')




