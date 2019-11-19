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
        self.market = 'bigone'
        #self.IS_TEST = True

    def trade_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self.trade_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def trade_get_thread(self, k_name=None, v_name=None):
        """
        
        :param k_name: 
        :param v_name: 
        :return: 
        """
        data_send = {"requestId": "1",
                     "subscribeMarketTradesRequest": {"market": v_name}}
        data_send = json.dumps(data_send)
        ws = create('wss://big.one/ws/v2',
                    header={'sec-websocket-protocol': 'json'},
                    subprotocols=['json'])
        ws.send(data_send)
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv.decode())
                tradeUpdate = data_recv.get('tradeUpdate')
                if tradeUpdate:
                    d = tradeUpdate['trade']
                    d['type'] = 'buy' if d['makerOrder'].get('side') else 'sell'
                    self.q.put({'symbol': k_name, 'data': d})
            except Exception as e:
                logger.warn('{} {} 最新交易获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random())
                        ws = create('wss://big.one/ws/v2',
                                    header={'sec-websocket-protocol': 'json'},
                                    subprotocols=['json'])
                        ws.send(data_send)
                        break
                    except Exception as e:
                        logger.warn(
                            '{} {} trade websocket异常{}'.format(self.market, k_name, e))
                        time.sleep(1)


if __name__ == '__main__':
    t = Trade()
    t.trade()