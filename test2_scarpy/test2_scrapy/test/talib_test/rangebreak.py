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
                      'symbol=f_usd_eos&type=1hour&contractType=quarter&limit=1000&coinVol=1'#quarter

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
    #print(data_kline)
    print(length)

    data = list(zip(data_kline.index, data_kline.high, data_kline.low, data_kline.close, data_kline.open))
    change = 0
    num = 0
    up_time = {}
    for d in data:
        high, low, close, open = d[1], d[2], d[3], d[4]
        signal = ''
        up = round(open + change*0.3, 3)
        down = round(open - change*0.3, 3)
        # c = high - low
        # if abs(c) >= 0.05:
        #     signal = '>>>>>>'
        #     num += 1
        #
        #     time_s = d[0].split()[-1]
        #     print(time_s)
        #     if time_s not in up_time:
        #         up_time[time_s] = 1
        #     else:
        #         up_time[time_s] += 1
        #     print(d, change, signal)
        # change = round(high - low, 3)
        # print(d, change, signal)
        if change!=0:
            signal = ''
            if high > up:
                signal += '>>>>>> '
            if low < down:
                signal += ' <<<<<<'
            num += 1

            # time_s = d[0].split()[-1]
            # print(time_s)
            # if time_s not in up_time:
            #     up_time[time_s] = 1
            # else:
            #     up_time[time_s] += 1
            # print(d, change, signal)
        change = abs(round(close - open, 3))
        if change <= 0.01:
            change = round(high - low, 3)
        print(d, change, signal, up, down)
    # print(num)
    # print(up_time)
    # for k, v in up_time.items():
    #     if v >= 5:
    #         print(k, v)


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