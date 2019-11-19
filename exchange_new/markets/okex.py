import sys
sys.path.append('/root/exchange_new')
import requests
import json
import time
from websocket import create_connection
import zlib
from markets.market_base import MarketBase

class Market(MarketBase):
    name = 'okex'
    exchange_rate_list = ['ETH_USDT','BTC_USDT','OKB_USDT']
    change_info = {'open':'open','close':'close','high':'high','low':'low','last':'last',
                       'change':'change','quoteVolume':'vol','baseVolume':'None'}

    def __init__(self):
        super().__init__()

    def market_update(self):
        """
        更新交易对
        :return: 
        """
        symbols = requests.get(
            'https://www.okex.me/api/spot/v3/instruments').json()
        mapping = {}
        for symbol in symbols:
            symbol = symbol.get('product_id')
            symbol = symbol.replace('-', '_')
            mapping[symbol] = symbol.lower()
        self.redis_2.hmset(self.market_name, mapping)
        self.logger.info('%s交易对更新完成' % (self.market_name))

        return True

    def data_get(self):
        """
        wss://real.okex.com:10441/websocket
        {'event':'addChannel','channel':'ok_sub_spot_usd_btc_ticker'}
        :return: 
        """
        self._data_get_commom(5)
        data_send_list = []
        for k,v in self.symbols.items():
            data_send_f = {'event': 'addChannel','channel': 'ok_sub_spot_usd_btc_ticker'}
            data_send_f['channel'] = 'ok_sub_spot_{v}_ticker'.format(v=v)
            data_send_list.append(data_send_f)
        data_send = json.dumps(data_send_list)

        ws = create_connection('wss://real.okex.com:10441/websocket')
        ws.send(data_send)

        while True:
            try:
                data_recv = ws.recv()
                data_recv = self.inflate(data_recv).decode()
                data_recv = json.loads(data_recv)
                for per in data_recv:
                    channel = per['channel']
                    if channel != 'addChannel':
                        symbol, data = channel[12:-7], per['data']
                        self.q.put({'symbol': symbol, 'data': data})
            except Exception as e:
                self.logger.warning('{} 最新价获取异常{}'.format(self.name, e))
                while True:
                    try:
                        ws = create_connection(
                            'wss://real.okex.com:10441/websocket')
                        ws.send(data_send)
                        break
                    except Exception as e:
                        self.logger.warning(
                            '{} ticker websocket异常{}'.format(self.name, e))
                        time.sleep(1)

    def _usd_update_other(self, ticker_new):
        """
        okex长连接返回的数据中没有baseVolume
        change数据不准确
        :param ticker_new: 
        :return: 
        """
        last_price, open_price = float(ticker_new['last']), float(ticker_new['open'])
        change = (last_price-open_price)/open_price*100
        ticker_new['change'] = change
        ticker_new['baseVolume'] = float(ticker_new['quoteVolume'])*last_price

        return ticker_new

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

    def symbols_get(self):
        """

        :return: 
        """
        symbols = requests.get(
            'https://www.okex.me/api/spot/v3/instruments').json()
        self.mapping = {}
        for symbol in symbols:
            symbol = symbol.get('product_id')
            symbol = symbol.replace('-', '_')
            self.mapping[symbol] = symbol.lower()


if __name__ == '__main__':
    m = Market()
    #m.market_update()
    #m.data_get()
    #m.ticker_new()
    m.symbols_check()
