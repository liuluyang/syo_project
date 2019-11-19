import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
from websocket import create_connection as create
import random
import gzip
from short_elves.kline_base import KlineBase

class Kline(KlineBase):

    def __init__(self):
        super().__init__()
        self.market = 'gateio'

    def kline_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def websocket_send(self, k_name, v_name):
        data_send = {"id": 12312, "method": "kline.subscribe",
                     "params": [k_name, 60]}
        data_send = json.dumps(data_send)
        # wss://webws.gateio.io/v3/
        # wss://ws.gateio.io/v3/
        ws = create("wss://webws.gateio.io/v3/")
        ws.send(data_send)
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = json.loads(data_recv)
        if data_recv.get('method') == 'kline.update':
            k = data_recv['params'][-1]
            open, close, kline_t = float(k[1]), float(k[2]), k[0]
            return open, close, kline_t
        else:
            return False

    def websocket_reconnection(self, data_send, k_name):
        ws = create("wss://webws.gateio.io/v3/")
        ws.send(data_send)
        return ws


if __name__ == '__main__':
    s = Kline()
    s.kline()