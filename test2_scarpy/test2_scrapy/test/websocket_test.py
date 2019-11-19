
from websocket import create_connection
import threading
import time
import json

def kline_get(num):
    data_send = {'market': 'gateio', 'method': 'kline', 'symbol': 'BCH_USDT',
                         'params': {'num': 2, 'period': 3600}, 'id': 1}
    data_send = json.dumps(data_send)

    while True:
        ws = create_connection('ws://47.75.223.85/v1/market/')
        ws.send(data_send)
        print(num, ws.recv())
        ws.close()
        time.sleep(0.5)

if __name__ == '__main__':
    for i in range(5):
        t = threading.Thread(target=kline_get, args=(i,))
        t.start()
