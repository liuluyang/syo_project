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
        self.market = 'bigone'
        #self.IS_TEST = True

    def kline_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def websocket_send(self, k_name, v_name):
        data_send = {"requestId": "1", "subscribeMarketCandlesRequest":
            {"market": v_name, "period": "MIN1"}}
        data_send = json.dumps(data_send)
        ws = create('wss://big.one/ws/v2',
                    header={'sec-websocket-protocol': 'json'},
                    subprotocols=['json'])
        ws.send(data_send)
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = json.loads(data_recv.decode())
        data_recv = data_recv.get('candleUpdate')
        if data_recv:
            k = data_recv['candle']
            open, close, kline_t = float(k['open']), float(k['close']), k['time']
            return open, close, kline_t
        else:
            return False

    def websocket_reconnection(self, data_send, k_name):
        time.sleep(random.random())
        ws = create('wss://big.one/ws/v2',
                    header={'sec-websocket-protocol': 'json'},
                    subprotocols=['json'])
        ws.send(data_send)
        return ws


if __name__ == '__main__':
    s = Kline()
    s.kline()