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
    high, low, close, date, open = data_kline.high, data_kline.low, data_kline.close, data_kline.index, data_kline.open
    percent = (close - open)/(high - low)
    print(percent)
    start = 0

    history = []
    n = 0
    profit = 0
    is_buy = 0
    buy_price = 0
    m = set()
    while True:
        end = start + 5
        if end > length:
            break
        highest, lowest = max(high[start:end]), min(low[start:end])
        x = highest - lowest
        p = abs(percent[end-1])
        price = close[end-1]
        change = price - open[end-1]
        d = date[end-1]
        up = int((price-lowest)/x*100)
        down = 100 - up
        signal = ''
        if up < 60 and not is_buy and p > 0.4:
            buy_price = price
            is_buy = 1
            n += 1
            print(d, up, down, price, change, signal, p)
        if up > 60 and is_buy:
            #profit += price - buy_price
            profit += buy_price - price
            m.add(buy_price - price)
            #m.add(price - buy_price)
            is_buy = 0
            #print(price - buy_price, buy_price)
        history.append((d, up, down, price, change, p))
        #print(d, up, down, price, change, signal, p)
        start += 1
    data = history[-2]
    global last_time
    if data[0] != last_time and data[-1] > 0.5:
        if data[1] < 30:
            print('开空')
            #main_3(type='2')
        elif data[1] > 70:
            print('开多')
            #main_3(type='1')
        last_time = data[0]
        print(last_time)
    print(n)
    print(profit, m, min(m), max(m))

#
# while True:
#     signal()
#     time.sleep(5)

if __name__ == '__main__':
    #s = SIGNAL()
    # t = threading.Thread(target=main_2)
    # t.start()
    while True:
        try:
            signal()
            time.sleep(5)
        except Exception as e:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            error = {'last_time':time_now, 'error':str(e)}
            data_redis(error)
            time.sleep(5)