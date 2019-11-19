import requests
import json
import threading
import time
from websocket import create_connection as create
from utils._logger import Logger as logger
import zlib
import random
from short_elves.trade_base import TradeBase

class Trade(TradeBase):

    def __init__(self):
        super().__init__()
        self.market = 'okex'

    def trade_get(self):
        t = threading.Thread(target=self.trade_get_thread)
        t.start()

    def trade_get_thread(self, k_name=None, v_name=None):
        data_send_list = []
        for k, v in self.symbols.items():
            data_send_f = {'event': 'addChannel','channel': 'ok_sub_spot_usd_btc_deals'}
            data_send_f['channel'] = 'ok_sub_spot_{v}_deals'.format(v=v)
            data_send_list.append(data_send_f)
        data_send_list = json.dumps(data_send_list)
        ws = create('wss://real.okex.com:10441/websocket')
        ws.send(data_send_list)

        while True:
            try:
                data_recv = ws.recv()
                data_recv = self.inflate(data_recv).decode()
                data_recv = json.loads(data_recv)
                for per in data_recv:
                    channel = per['channel']
                    data = per.get('data', None)
                    if channel != 'addChannel' and isinstance(data, list):
                        symbol = channel[12:-6].upper()
                        for d in data:
                            d_new = {}
                            d_new['amount'] = d[2]
                            d_new['price'] = d[1]
                            d_new['type'] = 'buy' if d[-1] == 'bid' else 'sell'
                            self.q.put({'symbol': symbol, 'data': d_new})
            except Exception as e:
                logger.warn('{} 最新交易获取异常{}'.format(self.market, e))
                while True:
                    try:
                        time.sleep(random.random())
                        ws = create('wss://real.okex.com:10441/websocket')
                        ws.send(data_send_list)
                        break
                    except Exception as e:
                        logger.warn(
                            '{} trade websocket异常{}'.format(self.market, e))
                        time.sleep(1)

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


if __name__ == '__main__':
    t = Trade()
    t.trade()