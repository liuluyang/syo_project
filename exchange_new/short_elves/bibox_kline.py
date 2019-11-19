import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
from websocket import create_connection as create
import random
import gzip
import base64
from short_elves.kline_base import KlineBase

class Kline(KlineBase):

    def __init__(self):
        super().__init__()
        self.market = 'bibox'
        #self.IS_TEST = True

    def kline_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def websocket_send(self, k_name, v_name):
        """
        k = {'time': 1541061360000, 'open': '0.00005278', 'high': '0.00005278', 
            'low': '0.00005278', 'close': '0.00005278', 'vol': '0'}
        :param k_name: 
        :param v_name: 
        :return: 
        """
        data_send = {
            "event": "addChannel",
            "channel": "bibox_sub_spot_{}_kline_1min".format(k_name)
        }
        data_send = json.dumps(data_send)
        ws = create('wss://push.bibox.com/')
        ws.send(data_send)
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = json.loads(data_recv)[0]
        data_type = data_recv.get('data_type')
        if data_type == 1:
            k = data_recv['data']
            k = self.inflate(k)[-1]
            open, close, kline_t = float(k['open']), float(k['close']), k['time']
            return open, close, kline_t
        else:
            return False

    def websocket_reconnection(self, data_send, k_name):
        time.sleep(random.random())
        ws = create('wss://push.bibox.com/')
        ws.send(data_send)
        return ws

    def inflate(self, data):
        """
        解压数据
        :param data: 
        :return: 
        """
        data = base64.b64decode(data)
        data = gzip.decompress(data)
        data = json.loads(data.decode())

        return data


if __name__ == '__main__':
    s = Kline()
    s.kline()