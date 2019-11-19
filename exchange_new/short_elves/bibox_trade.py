import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
from websocket import create_connection as create
from utils._logger import Logger as logger
import gzip
import random
import base64
from short_elves.trade_base import TradeBase

class Trade(TradeBase):

    def __init__(self):
        super().__init__()
        self.market = 'bibox'
        #self.IS_TEST = True

    def trade_get(self):
        self.keep_connection()
        for k, v in self.symbols.items():
            t = threading.Thread(target=self.trade_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def trade_get_thread(self, k_name=None, v_name=None):
        """
        d = {'pair': 'BTC_USDT', 'time': 1541124329985, 'price': 6440.4308, 
            'amount': 0.58803437, 'side': 2, 'id': 107255427}
        :param k_name: 
        :param v_name: 
        :return: 
        """
        data_send = {
            "event": "addChannel",
            "channel": "bibox_sub_spot_{}_deals".format(k_name)
        }
        data_send = json.dumps(data_send)
        ws = create('wss://push.bibox.com/')
        ws.send(data_send)
        self.ws_objs[k_name] = ws
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                if isinstance(data_recv, dict) and data_recv.get('pong'):
                    continue
                data_recv = data_recv[0]
                data_type = data_recv.get('data_type')
                if data_type == 1:
                    data = data_recv['data']
                    data = self.inflate(data)
                    for d in data:
                        d['type'] = 'buy' if d['side'] == 1 else 'sell'
                        self.q.put({'symbol': k_name, 'data': d})
            except Exception as e:
                logger.warn('{} {} 最新交易获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random() * 10)
                        ws = create('wss://push.bibox.com/')
                        ws.send(data_send)
                        self.ws_objs[k_name] = ws
                        break
                    except Exception as e:
                        logger.warn(
                            '{} {} trade websocket异常{}'.format(self.market, k_name, e))
                        time.sleep(1)

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
                        ws.send('{"ping":1}')
                        time.sleep(0.1)
                    except Exception as e:
                        logger.warning(
                            '{} {} websocket ping异常 {}'.format(self.market,
                                                            symbol, e))
        t = threading.Thread(target=ping)
        t.start()


if __name__ == '__main__':
    t = Trade()
    t.trade()