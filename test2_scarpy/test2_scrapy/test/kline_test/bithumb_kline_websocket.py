from websocket import create_connection
import json
import time


data_send = {"currency":"BTC","service":"transaction"}
data_send = json.dumps(data_send)
ws = create_connection('wss://wss.bithumb.com/public')
ws.send(data_send)

while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    print(data_recv.get('header'))
    if 'BTC' in data_recv.get('data', {}):
        print(data_recv)