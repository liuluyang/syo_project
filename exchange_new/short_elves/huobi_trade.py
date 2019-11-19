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
        self.market = 'huobi'

    def trade_get(self):
        for k, v in self.symbols.items():
            t = threading.Thread(target=self.trade_get_thread, args=(k, v))
            t.start()
            time.sleep(0.1)

    def trade_get_thread(self, k_name=None, v_name=None):
        data_send = {"sub": "market.{}.trade.detail".format(v_name)}
        data_send = json.dumps(data_send)
        ws = create('wss://api.huobi.pro/ws')
        ws.send(data_send)
        while True:
            try:
                data_recv = ws.recv()
                data_recv = gzip.decompress(data_recv).decode('utf8')
                data_recv = json.loads(data_recv)
                if data_recv.get('ping'):
                    ws.send(json.dumps({'pong': data_recv.get('ping')}))
                else:
                    data = data_recv.get('tick', {}).get('data', None)
                    if data:
                        for d in data:
                            d['type'] = 'buy' if d['direction'] == 'buy' else 'sell'
                            self.q.put({'symbol': k_name, 'data': d})
            except Exception as e:
                logger.warn('{} {} 最新交易获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random()*10)
                        ws = create('wss://api.huobi.pro/ws')
                        ws.send(data_send)
                        break
                    except Exception as e:
                        logger.warn(
                            '{} {} trade websocket异常{}'.format(self.market, k_name, e))
                        time.sleep(1)


if __name__ == '__main__':
    t = Trade()
    t.trade()