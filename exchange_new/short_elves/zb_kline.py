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
        self.market = 'zb'
        self.IS_TEST = True
        self.symbol_change = {'bchusdt': 'bccusdt', 'bchbtc': 'bccbtc',
                              'bchzb': 'bcczb', 'bchpax': 'bccpax',
                              'hcusdt': 'hsrusdt', 'hcbtc': 'hsrbtc',
                              'hczb': 'hsrzb','hcqc':'hsrqc','bchqc':'bccqc'}

    def kline_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.5)

    def websocket_send(self, k_name, v_name):
        symbol_new = self.symbol_change.get(v_name)
        data_send = {'event': 'addChannel',
                     'channel': '{}_kline_1min'.format(
                         v_name if not symbol_new else symbol_new)}
        data_send = json.dumps(data_send)
        ws = create('wss://kline.zb.cn/websocket')
        ws.send(data_send)
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = json.loads(data_recv)
        if data_recv.get('isSuc'):
            data = data_recv.get('datas', {}).get('data')
            k = data[-1]
            open, close, kline_t = float(k[1]), float(k[-2]), k[0]
            return open, close, kline_t
        else:
            return False

    def websocket_reconnection(self, data_send, k_name):
        time.sleep(random.random() * 10)
        ws = create('wss://kline.zb.cn/websocket')
        ws.send(data_send)
        return ws


if __name__ == '__main__':
    s = Kline()
    s.kline()