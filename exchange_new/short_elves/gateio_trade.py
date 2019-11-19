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
        self.market = 'gateio'

    def trade_get(self):
        t = threading.Thread(target=self.trade_get_thread)
        t.start()

    def trade_get_thread(self, k_name=None, v_name=None):
        # wss://webws.gateio.io/v3/
        # wss://ws.gateio.io/v3/
        ws = create("wss://webws.gateio.io/v3/")
        data_send_f = {"id":12312, "method":"trades.subscribe", "params":["ETH_USDT", "BTC_USDT"]}
        data_send_f['params'] = list(self.symbols.keys())
        data_send = json.dumps(data_send_f)
        ws.send(data_send)
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                if data_recv.get('method')=='trades.update':
                    symbol, data = data_recv['params'][0], data_recv['params'][1]
                    if symbol in self.trade_times:
                        for d in data:
                            self.q.put({'symbol': symbol, 'data': d})
                    else:
                        self.trade_times[symbol] = 1
            except Exception as e:
                logger.warn('{} 最新交易获取异常{}'.format(self.market, e))
                while True:
                    try:
                        time.sleep(random.random())
                        ws = create("wss://webws.gateio.io/v3/")
                        ws.send(data_send)
                        self.trade_times = {}
                        break
                    except Exception as e:
                        logger.warn(
                            '{} trade websocket异常{}'.format(self.market, e))
                        time.sleep(1)


if __name__ == '__main__':
    t = Trade()
    t.trade()