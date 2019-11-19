import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
from websocket import create_connection

from markets.market_base import MarketBase

class Market(MarketBase):
    name = 'gateio'
    exchange_rate_list = ['ETH_USDT','BTC_USDT']
    change_info = {'open':'open','close':'close','high':'high','low':'low',
                   'last':'last','change':'change','quoteVolume':'quoteVolume',
                   'baseVolume':'baseVolume'}

    def __init__(self):
        super().__init__()

    def symbol_filter(self, symbol):
        not_need_symbols = {'HT_USDT', 'BNB_USDT', 'MEETONE_ETH', 'ADD_ETH'}
        if symbol.endswith('CNYX') or symbol.endswith('QTUM'):
            return False
        if symbol.startswith('LLT'):
            return False
        if symbol in not_need_symbols:
            return False

        return True

    def market_update(self):
        markets = requests.get('https://data.gateio.io/api2/1/pairs').json()
        mapping = {}
        for market in markets:
            is_need = self.symbol_filter(market)
            if not is_need:
                continue
            mapping[market] = market
        self.redis_2.hmset(self.market_name, mapping)
        self.logger.info('%s交易对更新完成'%(self.market_name))

        return True

    def data_get(self):
        """
        
        :return: 
        """
        self._data_get_commom(5)
        # wss://webws.gateio.io/v3/
        # wss://ws.gateio.io/v3/
        ws = create_connection("wss://webws.gateio.io/v3/")
        data_send_f = {"id": 1, "method": "ticker.subscribe","params": []}
        data_send_f['params'] = list(self.symbols.keys())
        data_send = json.dumps(data_send_f)
        ws.send(data_send)

        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                if data_recv.get('method') == 'ticker.update':
                    symbol, data = data_recv['params'][0], data_recv['params'][1]
                    self.q.put({'symbol':symbol, 'data':data})
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                while True:
                    try:
                        ws = create_connection("wss://webws.gateio.io/v3/")
                        ws.send(data_send)
                        break
                    except Exception as e:
                        self.logger.warning(
                            '{} ticker websocket异常{}'.format(self.name, e))
                        time.sleep(1)

    def symbols_get(self):
        """
        
        :return: 
        """
        markets = requests.get('https://data.gateio.io/api2/1/pairs').json()
        self.mapping = {}
        for market in markets:
            is_need = self.symbol_filter(market)
            if not is_need:
                continue
            self.mapping[market] = market


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()

