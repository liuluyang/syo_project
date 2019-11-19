import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
from websocket import create_connection

from markets.market_base import MarketBase
from utils.Utils_huobi import get_symbols

class Market(MarketBase):
    name = 'huobi'
    exchange_rate_list = ['ETH_USDT','BTC_USDT','HT_USDT']
    change_info = {'open':'open','close':'close','high':'high','low':'low','last':'close',
                       'change':'None','quoteVolume':'amount','baseVolume':'vol'}

    def __init__(self):
        super().__init__()

    def symbol_filter(self, symbol):
        not_need_symbols = {'BT1_BTC', 'BT2_BTC'}
        if symbol.endswith('HUSD'):
            return False
        if symbol.startswith('CDC') or symbol.startswith('VEN'):
            return False
        if symbol in not_need_symbols:
            return False

        return True

    def market_update(self):
        """
        {'base-currency': 'btc', 'quote-currency': 'usdt', 'price-precision': 2,
        'amount-precision': 4, 'symbol-partition': 'main', 'symbol': 'btcusdt'}
        :return: 
        """
        try:
            data = get_symbols()
            symbols = data['data']
            mapping = {}
            for obj in symbols:
                sym_cur = '{}_{}'.format(obj['base-currency'], obj['quote-currency'])
                key, value = sym_cur.upper(), obj['symbol']
                is_need = self.symbol_filter(key)
                if not is_need:
                    continue
                mapping[key] = value
            self.redis_2.hmset(self.market_name, mapping)
            self.logger.info('%s交易对更新完成' % (self.market_name))
        except Exception as e:
            self.logger.warning('%s交易对更新异常:%s' % (self.name, e))

        return True

    def data_get(self):
        """
        {'open': 0.0198, 'close': 0.0204, 'low': 0.0193, 'high': 0.021, 
        'amount': 19654771.81686102, 'count': 4622, 'vol': 397419.68270820694, 
        'symbol': 'socusdt'}
        :return: 
        """
        self._data_get_commom(5)
        while True:
            try:
                url = 'https://api.huobi.pro/market/tickers'
                data_recv = requests.get(url, headers={
                    'content-type': 'application/x-www-form-urlencoded'},
                                         timeout=5)
                status_code = data_recv.status_code
                data_recv = data_recv.json()
                if status_code==200 and data_recv.get('status', None)=='ok':
                    for data in data_recv['data']:
                        symbol, data = data['symbol'], data
                        self.q.put({'symbol': symbol, 'data': data})
                else:
                    self.logger.warning(
                        '{} 最新价获取异常1{}'.format(self.name, json.dumps(data_recv)))
                time.sleep(1)
            except Exception as e:
                self.logger.warning('{} 最新价获取异常2{}'.format(self.name, e))
                time.sleep(2)

    def _usd_update_other(self, ticker_new):
        """
        huobi长连接返回的数据中没有change
        :param ticker_new: 
        :return: 
        """
        try:
            last_price, open_price = float(ticker_new['last']), float(ticker_new['open'])
            change = (last_price-open_price)/open_price*100
            ticker_new['change'] = change
        except Exception as e:
            ticker_new['change'] = 0

        return ticker_new

    def symbols_get(self):
        """

        :return: 
        """
        data = get_symbols()
        symbols = data['data']
        self.mapping = {}
        for obj in symbols:
            sym_cur = '{}_{}'.format(obj['base-currency'],
                                     obj['quote-currency'])
            key, value = sym_cur.upper(), obj['symbol']
            is_need = self.symbol_filter(key)
            if not is_need:
                continue
            self.mapping[key] = value


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()

