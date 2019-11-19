import requests
import threading
import time
import json
from websocket import create_connection


"""
{'datas': {'data': [[1541639760000, 6571.11, 6571.96, 6569.39, 6570.96, 32.7256]]}, 
'des': '', 'isSuc': True, 'channel': 'btcusdt_kline_1min'}
"""

def data_get(num):
    ws = create_connection('wss://kline.zb.cn/websocket')
    ws.send("{'event':'addChannel','channel':'btcusdt_kline_1min'}")
    while True:
        try:
            data = ws.recv()
            data = json.loads(data)
            print(num, data['isSuc'], data)
        except Exception as e:
            print('error:',e)
            ws = create_connection('wss://kline.zb.cn/websocket')
            ws.send("{'event':'addChannel','channel':'btcusdt_kline_1min'}")



if __name__ == '__main__':
    num = 0
    for i in range(1):
        num = i
        t = threading.Thread(target=data_get, args=(num,))
        t.start()
        time.sleep(1)
