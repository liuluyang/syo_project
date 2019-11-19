import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
from websocket import create_connection

from markets.market_base import MarketBase
from utils.bigone.client import Client

class Market(MarketBase):
    name = 'bigone'
    exchange_rate_list = ['EOS_USDT','BTC_USDT','ETH_USDT']
    change_info = {'open':'open','close':'close','high':'high','low':'low',
                   'last':'close','change':'daily_change_perc','quoteVolume':'volume',
                   'baseVolume':'None'}

    def __init__(self):
        super().__init__()
        self.api_key = 'bigone_api_key'
        self.api_secret = 'bigone_api_secret'

    def market_update(self):
        client = Client(self.api_key, self.api_secret)
        symbols = client.get_markets()
        mapping = {}
        for symbol in symbols:
            name = symbol['name']
            mapping[name.replace('-', '_')] = name
        self.redis_2.hmset(self.market_name, mapping)
        self.logger.info('%s交易对更新完成'%(self.market_name))

        return True

    def data_get(self):
        """
        {'volume': '576.44648', 'open': '6543.79', 'market_uuid': 
        '550b34db-696e-4434-a126-196f827d9172', 'market_id': 'BTC-USDT', 
        'low': '6509.23', 'high': '6725.39', 'daily_change_perc': 
        '0.07197663739209235015182333174', 'daily_change': '4.71', 
        'close': '6548.5', 'bid': {'price': '6550', 'amount': '0.01667'}, 
        'ask': {'price': '6550.08', 'amount': '0.02'}}
        :return: 
        """
        self._data_get_commom(5)
        client = Client(self.api_key, self.api_secret)
        updated_check = {}
        while True:
            try:
                tickers = client.get_tickers()
                for ticker in tickers:
                    market_id = ticker['market_id']
                    change_close = ticker['daily_change']+','+ticker['close']+\
                        ','+ticker['volume']
                    check_info = updated_check.get(market_id)
                    if not check_info or check_info != change_close:
                        symbol, data = market_id, ticker
                        self.q.put({'symbol': symbol, 'data': data})
                        #print(symbol, check_info, change_close, data)
                    updated_check[market_id] = change_close
                time.sleep(2)
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                time.sleep(2)

    def _usd_update_other(self, ticker_new):
        """
        http请求返回的数据中没有baseVolume
        :param ticker_new: 
        :return: 
        """
        last_price = float(ticker_new['last'])
        ticker_new['baseVolume'] = float(ticker_new['quoteVolume'])*last_price

        return ticker_new


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()

