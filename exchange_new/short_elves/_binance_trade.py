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
        self.market = 'binance'

    def trade_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self.trade_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def trade_get_thread(self, k_name=None, v_name=None):
        ws = create('wss://stream.binance.com:9443/ws/{}@trade'.format(v_name.lower()))
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                data_recv['price'] = data_recv['p']
                data_recv['amount'] = data_recv['q']
                data_recv['type'] = 'buy' if not data_recv['m'] else 'sell'
                self.q.put({'symbol': k_name, 'data': data_recv})
            except Exception as e:
                logger.warn('{} {} 最新交易获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random())
                        ws = create('wss://stream.binance.com:9443/ws/{}@trade'.
                                    format(v_name.lower()))
                        break
                    except Exception as e:
                        logger.warn(
                            '{} {} trade websocket异常{}'.format(self.market, k_name, e))
                        time.sleep(1)


if __name__ == '__main__':
    t = Trade()
    t.trade()