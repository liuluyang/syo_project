import sys
sys.path.append('/root')
import talib
import numpy as np
import pandas as pd
import json
import time
import requests
import redis
import threading
from test2_scrapy.test.talib_test.IndexTool import IndexTool
from test2_scrapy.test.talib_test.futures_order_new import main, main_2


def data_redis(data):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    last_time = data['last_time']
    if not r.sismember('trans_set_new', last_time):
        data = json.dumps(data)
        r.lpush('trans_new', data)
        r.sadd('trans_set_new', last_time)


def futures_price():
    futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                  'symbol=f_usd_eos&type=5min&contractType=quarter&limit=100&coinVol=1'
    data = requests.get(futures_url).json()
    data = data['data']

    return data[-1][-2]


class SIGNAL(object):

    def __init__(self):
        self.profit = 0
        self.is_buy = 0
        self.buy_price = 0
        self.profit_list = []

    def signal(self):
        it = IndexTool()

        """
        kline数据获取
        """

        def data_kline_get():
            spot_url = 'https://www.okex.me/v2/spot/markets/kline?' \
                       'symbol=eos_usdt&type=3min&limit=1000&coinVol=0'
            futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                          'symbol=f_usd_eos&type=5min&contractType=quarter&limit=1000&coinVol=1'

            url_dict = {'spot':spot_url, 'futures':futures_url}
            url_type = 'spot'
            data = requests.get(url_dict[url_type]).json()
            data = data['data']
            position_dict = {0:'createdDate',1:'close',2:'high',3:'low',4:'open',5:'volume'}
            data_new = []
            if url_type == 'spot':
                for d in data:
                    d_new = []
                    for i in range(0, 6):
                        d_new.append(float(d[position_dict[i]]))
                    d_new[0] = time.strftime('%Y-%m-%d %X', time.localtime(d_new[0] / 1000))
                    data_new.append(d_new)
            else:
                for d in data:
                    d[1], d[4] = d[4], d[1]
                    d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0] / 1000))
                    data_new = data


            dataFrame = pd.DataFrame(data_new, columns=['date', 'close', 'high', 'low', 'open',
                                                    'volume'])
            dataFrame.index = dataFrame.date
            dataFrame = dataFrame.iloc[:, 1:]

            return dataFrame

        data_kline = data_kline_get()
        last_price = futures_price()
        dif, dea, macd = it.MACD(data_kline)

        ema7, ema30 = it.EMA(data_kline, [7, 30])
        ema_x = ema7 - ema30

        sar = it.SAR(data_kline)
        sar_x = data_kline.close - sar

        signal = pd.Series(0.0, index=data_kline.index)
        for i in range(len(data_kline)):
            num = 0
            if dif[i] > 0:
                num += 1
            else:
                num -= 1
            if macd[i] > 0:
                num += 1
            else:
                num -= 1

            if ema_x[i] > 0:
                num += 1
            else:
                num -= 1

            if sar_x[i] > 0:
                num += 1
            else:
                num -= 1
            signal[i] = num

        date_ = signal.index[100:]
        signal = signal[100:]
        open = data_kline.open[100:]
        last_time = date_[-1]
        self.signal_text = ''
        self.p = 0
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        signal_data = {'last_time':last_time, 'last_price':last_price,
                       'signal_text':self.signal_text, 'p':self.p,
                       'time_now':time_now}
        print(time_now)
        for index, data in enumerate(list(zip(date_, signal, open))):
            date, sig, price = data
            price = last_price
            #print(data)
            sig_b = signal[index - 1]
            if index == 0:
                continue
            if date != last_time:
                continue
            if self.is_buy == 0:
                if sig > 0:
                    self.signal_text = '看多'
                    print('看多')
                    self.is_buy = 1
                    self.buy_price = price
                    main(type='1')
                elif sig < 0:
                    self.signal_text = '看空'
                    print('看空')
                    self.is_buy = -1
                    self.buy_price = price
                    main(type='2')
            else:
                if (self.is_buy==1 and sig_b > sig) or (self.is_buy==1 and sig == -4):
                    self.signal_text = '平多 开空'
                    print('平多 开空')
                    self.p = (price - self.buy_price) / price
                    print(self.p * 100)
                    self.is_buy = -1
                    self.buy_price = price
                    main(type='3')
                    main(type='2')
                elif (self.is_buy==-1 and sig_b < sig) or (self.is_buy==-1 and sig == 4):
                    self.signal_text = '平空 开多'
                    print('平空 开多')
                    self.p = (self.buy_price - price) / self.buy_price
                    print(self.p * 100)
                    self.is_buy = 1
                    self.buy_price = price
                    main(type='4')
                    main(type='1')

            if self.signal_text:
                signal_data['signal_text'] = self.signal_text
                signal_data['p'] = self.p
                data_redis(signal_data)


if __name__ == '__main__':
    s = SIGNAL()
    t = threading.Thread(target=main_2)
    t.start()
    while True:
        try:
            s.signal()
            time.sleep(5)
        except Exception as e:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            error = {'last_time':time_now, 'error':str(e)}
            data_redis(error)
            time.sleep(5)