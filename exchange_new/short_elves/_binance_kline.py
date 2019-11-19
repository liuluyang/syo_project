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
        self.market = 'binance'

    def kline_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def websocket_send(self, k_name, v_name):
        data_send = v_name.lower()
        ws = create('wss://stream.binance.com:9443/ws/{}@kline_1m'.format(
            data_send))
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = json.loads(data_recv)
        k = data_recv['k']
        open, close, kline_t = float(k['o']), float(k['c']), k['t']
        return open, close, kline_t

    def websocket_reconnection(self, data_send, k_name):
        ws = create('wss://stream.binance.com:9443/ws/{}@kline_1m'.
                    format(data_send))
        return ws


if __name__ == '__main__':
    s = Kline()
    s.kline()