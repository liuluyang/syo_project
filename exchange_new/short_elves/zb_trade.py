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
from short_elves.trade_base import TradeBase

class Trade(TradeBase):

    def __init__(self):
        super().__init__()
        self.market = 'zb'
        self.IS_TEST = True
        self.symbol_change = {'bchusdt': 'bccusdt', 'bchbtc': 'bccbtc',
                              'bchzb': 'bcczb', 'bchpax': 'bccpax',
                              'hcusdt': 'hsrusdt', 'hcbtc': 'hsrbtc',
                              'hczb': 'hsrzb','hcqc':'hsrqc','bchqc':'bccqc'}

    def trade_get(self):
        self.keep_connection()
        for k, v in self.symbols.items():
            t = threading.Thread(target=self.trade_get_thread, args=(k, v))
            t.start()
            time.sleep(0.5)

    def trade_get_thread(self, k_name=None, v_name=None):
        trade_times = {}
        symbol_new = self.symbol_change.get(v_name)
        data_send = {'event': 'addChannel', 'channel': '{}_trades'.format(
            v_name if not symbol_new else symbol_new)}
        data_send = json.dumps(data_send)
        ws = create('wss://api.zb.cn:9999/websocket')
        ws.send(data_send)
        self.ws_objs[k_name] = ws
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                data = data_recv.get('data')
                if data:
                    if k_name in trade_times:
                        for d in data:
                            self.q.put({'symbol': k_name, 'data': d})
                    else:
                        trade_times[k_name] = 1
            except Exception as e:
                logger.warn('{} {} 最新交易获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random() * 20)
                        ws = create('wss://api.zb.cn:9999/websocket')
                        ws.send(data_send)
                        trade_times = {}
                        self.ws_objs[k_name] = ws
                        break
                    except Exception as e:
                        logger.warn(
                            '{} trade websocket异常{}'.format(self.market, e))
                        time.sleep(1)

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
                        ws.send('{"ping":"123"}')
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