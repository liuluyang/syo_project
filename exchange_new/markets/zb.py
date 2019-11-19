import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
import random
from websocket import create_connection

from markets.market_base import MarketBase

class Market(MarketBase):
    name = 'zb'
    exchange_rate_list = ['ZB_USDT','BTC_USDT','PAX_USDT']
    change_info = {'open':'open','close':'last','high':'high','low':'low',
                   'last':'last','change':'change','quoteVolume':'vol',
                   'baseVolume':'None'}

    def __init__(self):
        super().__init__()
        self.symbol_change = {'bchusdt':'bccusdt','bchbtc':'bccbtc',
                              'bchzb':'bcczb','bchpax':'bccpax',
                              'hcusdt':'hsrusdt','hcbtc':'hsrbtc',
                              'hczb':'hsrzb','hcqc':'hsrqc','bchqc':'bccqc'}

    def symbol_filter(self, symbol):
        not_need_symbols = {}
        if symbol.startswith('bcc_') or symbol.startswith(
                'hsr_') or symbol.startswith('bch_'):
            return False
        if symbol in not_need_symbols:
            return False

        return True

    def market_update(self):
        symbols = requests.get('http://api.zb.cn/data/v1/markets').json()
        mapping = {}
        for symbol in symbols.keys():
            is_need = self.symbol_filter(symbol)
            if not is_need:
                continue
            mapping[symbol.upper()] = ''.join(symbol.split('_'))
        self.redis_2.hmset(self.market_name, mapping)
        self.logger.info('%s交易对更新完成'%(self.market_name))

        return True

    def data_get(self):
        """
        {"vol":"8595.9216","last":"6564.57","sell":"6564.5","buy":"6561.71",
        "high":"6608.03","low":"6533.63"}
        :return: 
        """
        self._data_get_commom(5)
        self.klines_24h()
        updated_check = {}
        symbols = set(self.symbols.values())
        while True:
            try:
                tickers = requests.get('http://api.zb.cn/data/v1/allTicker').json()
                for symbol, ticker in tickers.items():
                    if symbol not in symbols:
                        continue
                    change_close = ticker['last'] + ',' + ticker['vol']
                    check_info = updated_check.get(symbol)
                    if not check_info or check_info != change_close:
                        ticker = self.ticker_update(ticker, symbol)
                        if not ticker:
                            continue
                        last_price = float(ticker['last'])
                        ticker['change'] = (last_price - ticker['open'])/\
                                           ticker['open']*100
                        symbol, data = symbol, ticker
                        self.q.put({'symbol': symbol, 'data': data})
                        #print(symbol, check_info, change_close, data)
                    updated_check[symbol] = change_close
                time.sleep(1)
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                time.sleep(2)

    def klines_24h(self):
        """
        
        :return:
        """
        self.tickers_open = {}
        tickers_open = self.redis_3.hgetall('zb_klines_24h')
        if tickers_open:
            self.tickers_open = {k.decode():json.loads(v.decode()) for
                                 k,v in tickers_open.items()}
        else:
            for k_name, v_name in self.symbols.items():
                open_price = self.kline_24h_get(v_name)
                if open_price:
                    ticker_open = {"open":open_price, "timestamp":time.time()}
                    self.tickers_open[v_name] = ticker_open
                    self.redis_3.hset('zb_klines_24h', v_name,
                                      json.dumps(ticker_open))
                time.sleep(0.5)

    def kline_24h_get(self, symbol):
        """
        
        :param symbol: 
        :return: open_price
        """
        time.sleep(random.random())
        try:
            symbol_new = self.symbol_change.get(symbol)
            data_send = {'event': 'addChannel',
                         'channel': '{}_kline_1hour'.format(
                             symbol if not symbol_new else symbol_new)}
            data_send = json.dumps(data_send)
            ws = create_connection('wss://kline.zb.cn/websocket')
            ws.send(data_send)

            data_recv = ws.recv()
            data_recv = json.loads(data_recv)
            if data_recv.get('isSuc'):
                #订阅成功
                data = data_recv.get('datas', {}).get('data')
                try:
                    open_price = data[-24][1]
                except:
                    open_price = data[-1][1]
                return open_price
            else:
                self.logger.warning(
                    'zb {}获取24小时开盘价websocket订阅异常'.format(symbol))
            ws.close()
        except Exception as e:
            self.logger.warning(
                'zb {}获取24小时开盘价异常 {}'.format(symbol, e))

        return False

    def ticker_update(self, ticker, symbol):
        """
        
        :param ticker: 
        :param symbol: 
        :return: 
        """
        ticker_open = self.tickers_open.get(symbol)
        if ticker_open and time.time() - ticker_open['timestamp'] < 3600:
            ticker['open'] = ticker_open['open']
            return ticker
        else:
            time.sleep(0.5)
            open_price = self.kline_24h_get(symbol)
            if open_price:
                ticker_open = {"open":open_price, "timestamp":time.time()}
                self.tickers_open[symbol] = ticker_open
                self.redis_3.hset('zb_klines_24h', symbol, json.dumps(ticker_open))
                ticker['open'] = open_price
                return ticker

        return False

    def _usd_update_other(self, ticker_new):
        """
        http请求返回的数据中没有baseVolume(交易额)
        :param ticker_new: 
        :return: 
        """
        ticker_new['last'] = float(ticker_new['last'])
        ticker_new['baseVolume'] = ticker_new['last']*float(ticker_new['quoteVolume'])

        return ticker_new

    def symbols_get(self):
        """

        :return: 
        """
        symbols = requests.get('http://api.zb.cn/data/v1/markets').json()
        self.mapping = {}
        for symbol in symbols.keys():
            is_need = self.symbol_filter(symbol)
            if not is_need:
                continue
            self.mapping[symbol.upper()] = ''.join(symbol.split('_'))


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()

