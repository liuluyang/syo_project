import talib
import numpy as np
import pandas as pd
import json
import time
from websocket import create_connection
import requests
import redis
import threading
from test2_scrapy.test.talib_test.futures_order_new import main, main_2, main_3
from test2_scrapy.test.talib_test.IndexTool import IndexTool


def data_redis(data):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    last_time = data['last_time']
    if not r.sismember('trans_set_new_0305', last_time):
        data = json.dumps(data)
        r.lpush('trans_new_0305', data)
        r.sadd('trans_set_new_0305', last_time)


last_time = 0
def signal():
    it = IndexTool()
    """
    kline数据获取
    """
    def data_kline_get():
        spot_url = 'https://www.okex.me/v2/spot/markets/kline?' \
                   'symbol=eos_usdt&type=5min&limit=1000&coinVol=0'

        futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                      'symbol=f_usd_eos&type=3min&contractType=quarter&limit=1000&coinVol=1'

        url_dict = {'spot':spot_url, 'futures':futures_url}
        url_type = 'futures'
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
    length = len(data_kline)
    #print(data_kline, length)
    # ma9 = round(it.MA(data_kline, period=9), 3)
    ema9 = round(it.EMA(data_kline, period=8), 3)
    ma9 = ema9
    high, low, close, date, open = data_kline.high, data_kline.low, data_kline.close, data_kline.index, data_kline.open
    percent = (close - open)/(high - low)
    change = close - open
    middle = round((close+open)/2, 3)

    start = 0
    scale = pd.Series(0.0, data_kline.index)
    true_change = pd.Series(0.0, data_kline.index)
    while True:
        end = start + 8
        if end > length:
            break
        highest, lowest = max(high[start:end]), min(low[start:end])
        x = highest - lowest
        price = close[end - 1]
        up = round((price - lowest) / x * 100, 2)
        scale[end-1] = up
        true_change[end-1] = x
        start += 1

    data = list(zip(data_kline.index, round(change, 3), round(percent, 2), scale, ma9, middle, close, true_change))

    num = 0
    date_range = []
    is_buy = 0
    buy_price = 0
    profit_list = []
    for d in data:
        c = d[7]
        price = d[6]
        if abs(d[1]) >= 0.004 and abs(d[2]) >= 0.4 and d[3] > 60 and d[5] > d[4]:
            if is_buy <= 0:
                date_range.append(d[0])
                is_buy = 1
                num += 1
                print('$$-多', 'true_change:', c)
                if buy_price != 0:
                    profit = buy_price - price
                    profit_list.append((d[0], profit))
                    print(profit)
                buy_price = price
        if abs(d[1]) >= 0.004 and abs(d[2]) >= 0.4 and d[3] < 40 and d[5] < d[4]:
            if is_buy >= 0:
                date_range.append(d[0])
                is_buy = -1
                num += 1
                print('$$-空', 'true_change:', c)
                if buy_price != 0:
                    profit = price - buy_price
                    profit_list.append((d[0], profit))
                    print(profit)
                buy_price = price
        print(d)
    print(num)

    profit_all = 0
    win = 0
    for p in profit_list:
        #print(p)
        if p[1] > 0:
            win += 1
        profit_all += p[1]
    print(profit_all, win)
    #print(sum(abs(change)))

    # print(scale)
    # print(len(scale))
    #print(ma9)
    #print(middle)

    #it.matplot((close, 'close'), date_range=date_range)


if __name__ == '__main__':
    while True:
        try:
            signal()
            time.sleep(5)
            #break
        except Exception as e:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            error = {'last_time':time_now, 'error':str(e)}
            data_redis(error)
            time.sleep(5)