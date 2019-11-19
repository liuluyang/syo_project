import requests
import threading
import time
import json
from websocket import create_connection

#ws_list = [create_connection('wss://kline.zb.cn/websocket') for i in range(10)]

#print (ws_list)

def data_get(num):
    ws = create_connection('wss://kline.zb.cn/websocket')
    ws.send("{'event':'addChannel','channel':'btcusdt_kline_1min'}")
    data = ws.recv()
    data = json.loads(data)
    print(num, data['datas']['data'])


if __name__ == '__main__':
    num = 0
    while True:
        num+=1
        t = threading.Thread(target=data_get, args=(num,))
        t.start()
        time.sleep(0.01)

