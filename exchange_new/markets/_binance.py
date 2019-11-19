import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
from binance.client import Client
from websocket import create_connection

from settings import api_key_b, api_secret_b
from markets.market_base import MarketBase

class Market(MarketBase):
    name = 'binance'
    exchange_rate_list = ['ETH_USDT','BTC_USDT','BNB_USDT']
    change_info = {'open':'o','close':'c','high':'h','low':'l','last':'c',
                    'change':'P','quoteVolume':'v','baseVolume':'q'}

    def __init__(self):
        super().__init__()
        self.api_key = api_key_b
        self.api_secret = api_secret_b

    def symbol_filter(self, symbol):
        not_need_symbols = {'SALT_BTC','SALT_ETH','SUB_BTC','SUB_ETH','MOD_BTC',
                            'MOD_ETH','WINGS_BTC','WINGS_ETH','CLOAK_BTC','CLOAK_ETH',
                            'PAX_BTC','PAX_BNB','PAX_ETH','USDC_BNB','USDC_BTC'}
        for s in ['HSR','VEN','ICN','TRIG','CHAT','RPX','BCN','BCC']:
            if symbol.startswith(s):
                return False
        if symbol in not_need_symbols:
            return False

        return True

    def _make_symbol(self, symbol):
        markets = ['BTC','BNB','ETH','USDT']
        for m in markets:
            if symbol.endswith(m):
                symbol = symbol[:-len(m)]+'_'+m
                return symbol

        return False

    def market_update(self):
        self.client = Client(self.api_key, self.api_secret)
        markets = self.client.get_all_tickers()
        for market in markets:
            symbol = market['symbol']
            symbol_new = self._make_symbol(symbol)
            if not symbol_new:
                continue
            is_need = self.symbol_filter(symbol_new)
            if not is_need:
                continue
            if symbol_new:
                self.redis_2.hset(self.market_name, symbol_new, symbol)
            else:
                self.logger.warning('%s交易对更新：发现异常交易对'%(self.name))
        self.logger.info('%s交易对更新完成'%(self.name))

        return True

    def data_get(self):
        """
        
        :return: 
        """
        self._data_get_commom(15)
        ws = create_connection('wss://stream.binance.com:9443/ws/!ticker@arr')
        while True:
            try:
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                for data in data_recv:
                    symbol, data = data['s'], data
                    self.q.put({'symbol': symbol, 'data': data})
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                while True:
                    try:
                        ws = create_connection(
                            'wss://stream.binance.com:9443/ws/!ticker@arr')
                        break
                    except Exception as e:
                        self.logger.warning(
                            '{} ticker websocket异常{}'.format(self.name, e))
                        time.sleep(1)

    def symbols_get(self):
        """

        :return: 
        """
        self.mapping = {}
        self.client = Client(self.api_key, self.api_secret)
        markets = self.client.get_all_tickers()
        for market in markets:
            symbol = market['symbol']
            symbol_new = self._make_symbol(symbol)
            if not symbol_new:
                continue
            is_need = self.symbol_filter(symbol_new)
            if not is_need:
                continue
            if symbol_new:
                self.mapping[symbol_new] = symbol


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()
