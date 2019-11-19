import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
from websocket import create_connection

from markets.market_base import MarketBase

class Market(MarketBase):
    name = 'bibox'
    exchange_rate_list = ['ETH_USDT','BTC_USDT','BIX_USDT','GUSD_USDT']
    change_info = {'open':'last','close':'last','high':'high','low':'low',
                   'last':'last','change':'percent','quoteVolume':'vol24H',
                   'baseVolume':'amount'}

    def __init__(self):
        super().__init__()

    def symbol_filter(self, symbol):
        remove_1214 = 'CAT_BTC,CAT_ETH,AIDOC_BTC,AIDOC_ETH,WAX_BTC,WAX_ETH,' \
                      'BLT_BTC,BLT_ETH,KICK_BTC,KICK_ETH,MED_BTC,MED_ETH'
        remove_1214 = remove_1214.split(',')
        remove_0116 = 'MT_BIX,MTC_BIX,RTE_BIX,SGC_BIX,TNB_BTC,PRA_BTC'
        remove_0116 = remove_0116.split(',')
        not_need_symbols = set(remove_1214)|set(remove_0116)
        if symbol.endswith('DAI'):
            return False
        if symbol in not_need_symbols:
            return False
        if symbol.startswith('TCT') or symbol.startswith('AC3'):
            return False

        return True

    def market_update(self):
        """
        ETH/DAI BTC/DAI暂未启用
        :return: 
        """
        symbols = requests.get('https://api.bibox.com/v1/mdata?cmd=pairList').json()
        symbols = symbols['result']
        mapping = {}
        for symbol in symbols:
            symbol = symbol['pair']
            is_need = self.symbol_filter(symbol)
            if not is_need:
                continue
            mapping[symbol] = symbol
        self.redis_2.hmset(self.market_name, mapping)
        self.logger.info('%s交易对更新完成'%(self.market_name))

        return True

    def data_get(self):
        """
        {'id': 1, 'coin_symbol': 'BIX', 'currency_symbol': 'BTC', 'is_hide': 0, 
        'last': '0.00005295', 'high': '0.00005475', 'low': '0.00005257', 
        'change': '-0.00000045', 'percent': '-0.84%', 'vol24H': '4423571', 
        'amount': '234.26', 'last_cny': '2.35', 'high_cny': '2.43', 
        'low_cny': '2.33', 'last_usd': '0.33', 'high_usd': '0.34', 
        'low_usd': '0.33'}
        :return: 
        """
        self._data_get_commom(5)
        updated_check = {}
        while True:
            try:
                tickers = requests.get(
                    'https://api.bibox.com/v1/mdata?cmd=marketAll').json()
                tickers = tickers.get('result')
                for ticker in tickers:
                    symbol = '{}_{}'.format(ticker['coin_symbol'],
                                            ticker['currency_symbol'])
                    change_close = ticker['change']+','+ticker['last']
                    check_info = updated_check.get(symbol)
                    if not check_info or check_info != change_close:
                        symbol, data = symbol, ticker
                        self.q.put({'symbol': symbol, 'data': data})
                        #print(symbol, check_info, change_close, data)
                    updated_check[symbol] = change_close
                time.sleep(1)
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                time.sleep(2)

    def _usd_update_other(self, ticker_new):
        """
        http请求返回的数据中没有open
        :param ticker_new: 
        :return: 
        """
        ticker_new['change'] = float(ticker_new['change'].replace('%', ''))
        ticker_new['last'] = float(ticker_new['last'])
        ticker_new['open'] = ticker_new['last']/(1+ticker_new['change']/100)

        return ticker_new

    def symbols_get(self):
        """

        :return: 
        """
        symbols = requests.get(
            'https://api.bibox.com/v1/mdata?cmd=pairList').json()
        symbols = symbols['result']
        self.mapping = {}
        for symbol in symbols:
            symbol = symbol['pair']
            is_need = self.symbol_filter(symbol)
            if not is_need:
                continue
            self.mapping[symbol] = symbol


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()

