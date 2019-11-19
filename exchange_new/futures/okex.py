import sys
sys.path.append('/root/exchange_new')
from websocket import create_connection
import threading
import requests
import time
import random
import json
import zlib
from utils._logger import Logger as logger
from utils._redis_link import redis_6


class OkexFutures(object):
    logger = logger
    redis_6 = redis_6

    def __init__(self):
        self.update_interval = 300 #秒
        self.symbols = 'btc,ltc,eth,etc,eos,xrp'.split(',')
        #季度溢价
        self.url_spot = 'https://www.okex.me/v2/market/index/kLine?' \
                   'symbol=f_usd_{}&type={}&limit={}&coinVol=0'
        self.url_future = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                     'symbol=f_usd_{}&type={}&limit={}&coinVol=1&contractType=quarter'
        #持仓总量
        self.url_position = 'https://www.okex.me/v2/futures/pc/public/' \
                            'futureVolume.do?symbol=f_usd_{}&type={}'
        #交易精英趋向指标
        self.scale_url = 'https://www.okex.me/v2/futures/pc/public/eliteScale.do?' \
                    'symbol=f_usd_{}&type={}'
        self.ratio_url = 'https://www.okex.me/v2/futures/pc/public/' \
                         'getFuturePositionRatio.do?symbol=f_usd_{}&type={}'

    def redis_storage(self, symbol, type, data):
        """
        数据存入redis
        :param symbol: 
        :param type: 
        :param data: 
        :return: 
        """
        if isinstance(data, dict):
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            data['updated_at'] = time_now
            data = json.dumps(data)
        else:
            raise ValueError('data is not dict')
        self.redis_6.hset(symbol, type, data)
        if type != 'price':
            updated_at = json.dumps({'time':time_now})
            self.redis_6.hset(symbol, 'updated_at', updated_at)

        return True

    def price(self):
        """
        合约指数 本周 下周 季度(价)
        :return: 
        """
        def inflate(data):
            decompress = zlib.decompressobj(
                -zlib.MAX_WBITS  # see above
            )
            inflated = decompress.decompress(data)
            inflated += decompress.flush()
            return inflated

        channels = {'this_week': 'ok_sub_futureusd_{}_ticker_this_week',
                    'next_week': 'ok_sub_futureusd_{}_ticker_next_week',
                    'quarter': 'ok_sub_futureusd_{}_ticker_quarter',
                    'index': 'ok_sub_futureusd_{}_index',
                    }
        data_send = []
        self.data_origin = {}
        for symbol in self.symbols:
            for type, channel in channels.items():
                channel = channel.format(symbol)
                self.data_origin[channel] = {'symbol': symbol, 'type': type,
                                        'data':None}
                data_send.append({'event': 'addChannel', 'channel': channel})
        data_send = json.dumps(data_send)
        ws = create_connection('wss://real.okex.com:10440/ws/v1')
        ws.send(data_send)

        while True:
            try:
                data_recv = ws.recv()
                data_recv = inflate(data_recv)
                data_recv = json.loads(data_recv.decode())[0]
                data_perm = self.data_origin.get(data_recv.get('channel'))
                if data_perm:
                    data_perm['data'] = data_recv.get('data')
            except Exception as e:
                self.logger.warning(
                    '<futures>-合约价格 数据获取异常{}'.format(e))
                while True:
                    try:
                        time.sleep(random.random() * 5)
                        ws = create_connection('wss://real.okex.com:10440/ws/v1')
                        ws.send(data_send)
                        break
                    except Exception as e:
                        self.logger.warning(
                            '<futures>-合约价格 websocket异常{}'.format(e))
                        time.sleep(1)

    def price_process(self):
        """
        价格数据处理
        :return: 
        """
        while True:
            data_new = {}
            for v in self.data_origin.values():
                symbol, type, data = v['symbol'], v['type'], v['data']
                if symbol not in data_new:
                    data_new[symbol] = {}
                if data:
                    if type == 'index':
                        price = float(data['futureIndex'])
                    else:
                        price = float(data['last'])
                    price = round(price, 2) if price >= 100 else round(price, 4)
                    data_new[symbol][type] = price
                    data_redis = data_new[symbol]
                    if len(data_redis) == 4:
                        self.redis_storage(symbol, 'price', data_redis)
            time.sleep(1)

    def price_main(self):
        """
        价格主函数
        :return: 
        """
        t1 = threading.Thread(target=self.price)
        t1.start()
        t2 = threading.Thread(target=self.price_process)
        t2.start()
        t1.join()
        t2.join()

    def position(self):
        """
        持仓总量
        :return: 
        """
        def data_process(data):
            data = data['data']
            data = [[d[0], round(d[1]/2, 2)] for d in data]
            return data

        intervals = {'1h':1, '4h':2, '12h':3}
        for symbol in self.symbols:
            try:
                data_redis = {}
                for k, type in intervals.items():
                    positionInfo = requests.get(
                        self.url_position.format(symbol, type)).json()
                    if positionInfo.get('msg') == 'success':
                        data_redis[k] = data_process(positionInfo)
                    else:
                        raise KeyError(json.dumps(positionInfo))
                    time.sleep(0.2)
                self.redis_storage(symbol, 'position', data_redis)
            except Exception as e:
                self.logger.warning(
                    '<futures>-持仓总量{} 数据获取异常{}'.format(symbol, e))

    def elite(self):
        """
        交易精英趋向指标
        scale -> 时间戳 做多 做空
        ratio -> 时间戳 多头 空头
        :return: 
        """
        def data_process(data):
            data = data['data']
            data = zip(data['timedata'], data['buydata'],
                             data['selldata'])
            data = [[int(d[0]), round(d[1] * 100, 2), round(d[2] * 100, 2)] for
                    d in data]
            return data

        intervals = {'5m': 0, '15m': 1, '1h': 2}
        for symbol in self.symbols:
            try:
                data_redis = {}
                for k, type in intervals.items():
                    scaleInfo = requests.get(self.scale_url.format(symbol, type)).json()
                    ratioInfo = requests.get(self.ratio_url.format(symbol, type)).json()
                    if scaleInfo.get('msg') == 'success':
                        data_scale = data_process(scaleInfo)
                    else:
                        raise KeyError(json.dumps(scaleInfo))
                    if ratioInfo.get('msg') == 'success':
                        data_ratio = data_process(ratioInfo)
                    else:
                        raise KeyError(json.dumps(ratioInfo))
                    data_redis[k] = {'scale':data_scale, 'ratio':data_ratio}
                    time.sleep(0.2)
                self.redis_storage(symbol, 'elite', data_redis)
            except Exception as e:
                self.logger.warning(
                    '<futures>-交易精英趋向指标{} 数据获取异常{}'.format(symbol, e))

    def futures_spots_kline(self):
        """
        季度溢价
        :return: 
        """
        day_1, day_3, week_1 = ('30min', 48), ('2hour', 36), ('6hour', 28)
        urls = [['spot',self.url_spot], ['future',self.url_future]]
        for symbol in self.symbols:
            try:
                data = []
                data_redis = {}
                for type, url in urls:
                    data_day = requests.get(
                        url.format(symbol, day_1[0], day_1[1])).json()
                    data_3day = requests.get(
                        url.format(symbol, day_3[0], day_3[1])).json()
                    data_week = requests.get(
                        url.format(symbol, week_1[0], week_1[1])).json()
                    data.append([data_day['data'], data_3day['data'], data_week['data']])
                    time.sleep(0.2)
                for index, type in enumerate(['day', '3day', 'week']):
                    spots, futures = data[0][index], data[1][index]
                    data_new = []
                    for d in zip(futures, spots):
                        timestamps = d[0][0]
                        future_price = d[0][-2]
                        spot_price = d[1][-2]
                        percent = (future_price-spot_price)/spot_price*100
                        percent = round(percent, 2)
                        data_new.append([timestamps, future_price, spot_price, percent])
                    data_redis[type] = data_new
                self.redis_storage(symbol, 'futures_spots_kline', data_redis)
            except Exception as e:
                self.logger.warning(
                    '<futures>-季度溢价{} 数据获取异常{}'.format(symbol, e))

    def data_chart_main(self):
        """
        图表数据主函数
        :return: 
        """
        def main():
            while True:
                self.futures_spots_kline()
                self.position()
                self.elite()
                time.sleep(self.update_interval)
        t = threading.Thread(target=main)
        t.start()
        t.join()

    def blastingOrders(self):
        """
        爆仓单
        :return: 
        """
        url_currency = 'https://test1.bicoin.info/stock/getOutOfStockList?' \
              'pageNum=1&pageSize=100&host=leekassit&symbolStr={}'
        url_all = 'https://test1.bicoin.info/stock/getOutOfStockList?' \
                  'pageNum=1&pageSize=200&host=leekassit'
        for symbol in self.symbols:
            try:
                ordersInfo = requests.get(url_currency.format(symbol), timeout=5)
                self.error_history(ordersInfo)
                ordersInfo = ordersInfo.json()
                if ordersInfo.get('code'):
                    data_redis = ordersInfo.get('data')
                    self.redis_storage(symbol, 'blastingOrders', data_redis)
                else:
                    self.logger.warning(
                        '<futures>-爆仓单{} 数据获取异常{}'.format(symbol,
                                                          json.dumps(ordersInfo)))
                    time.sleep(random.random() * 10)
                time.sleep(2 + random.random())
            except Exception as e:
                self.logger.warning(
                    '<futures>-爆仓单{} 数据获取异常{}'.format(symbol, e))
        try:
            ordersAll = requests.get(url_all, timeout=5).json()
            if ordersAll.get('code'):
                data_redis = ordersAll.get('data')
                time_now = time.strftime('%Y-%m-%d %X', time.localtime())
                data_redis['updated_at'] = time_now
                self.redis_6.hset('global', 'blastingOrders', json.dumps(data_redis))
            else:
                self.logger.warning(
                    '<futures>-爆仓单ALL 数据获取异常{}'.format(json.dumps(ordersAll)))
                time.sleep(random.random() * 10)
        except Exception as e:
            self.logger.warning(
                '<futures>-爆仓单ALL 数据获取异常{}'.format(e))

    def blastingOrders_main(self):
        while True:
            t = threading.Thread(target=self.blastingOrders)
            t.start()
            time.sleep(random.random()*10 + 50)

    def error_history(self, response):
        """
        记录爆仓请求历史
        :param response: 
        :return: 
        """
        status_code = response.status_code
        text = response.text
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        result = {'status_code':status_code, 'updated_at':time_now, 'text':text}
        self.redis_6.lpush('error_history', json.dumps(result))


if __name__ == '__main__':
    o = OkexFutures()
    # o.data_chart_main()
    # o.price_main()
    #o.blastingOrders()
    o.blastingOrders_main()