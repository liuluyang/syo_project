import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
from websocket import create_connection as create
import random
import zlib
from short_elves.kline_base import KlineBase
from utils._logger import Logger as logger

class Kline(KlineBase):

    def __init__(self):
        super().__init__()
        self.market = 'okex'

    def kline_get(self):
        self.keep_connection()
        for k, v in self.symbols.items():
            t = threading.Thread(target=self._kline_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def websocket_send(self, k_name, v_name):
        data_send = {'event': 'addChannel',
                     'channel': 'ok_sub_spot_{}_kline_1min'.format(
                         k_name.lower())}
        data_send = json.dumps(data_send)
        ws = create('wss://real.okex.com:10441/websocket')
        ws.send(data_send)
        self.ws_objs[k_name] = ws
        return ws, data_send

    def websocket_recv(self, ws):
        data_recv = ws.recv()
        data_recv = self.inflate(data_recv).decode()
        data_recv = json.loads(data_recv)
        if isinstance(data_recv, dict) and data_recv.get('event') == 'pong':
            return False
        data_recv = data_recv[-1]
        channel = data_recv['channel']
        data = data_recv.get('data', None)
        if channel != 'addChannel' and isinstance(data, list):
            k = data[-1]
            open, close, kline_t = float(k[1]), float(k[-2]), k[0]
            return open, close, kline_t
        else:
            return False

    def websocket_reconnection(self, data_send, k_name):
        time.sleep(random.random()*10)
        ws = create('wss://real.okex.com:10441/websocket')
        ws.send(data_send)
        self.ws_objs[k_name] = ws
        return ws

    def inflate(self, data):
        """
        解压数据
        :param data: 
        :return: 
        """
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated

    def keep_connection(self):
        """
        发送心跳包 保持连接
        :return: 
        """
        self.ws_objs = {}
        def ping():
            while True:
                time.sleep(10)
                for symbol, ws in list(self.ws_objs.items()):
                    try:
                        ws.send('{"event":"ping"}')
                        time.sleep(0.05)
                    except Exception as e:
                        logger.warning(
                            '{} {} websocket ping异常 {}'.format(self.market,
                                                            symbol, e))
        t = threading.Thread(target=ping)
        t.start()


if __name__ == '__main__':
    s = Kline()
    s.kline()