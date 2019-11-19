import sys
sys.path.append('/root/okex_futures_5')
import talib
import numpy as np
import pandas as pd
import json
import time
import requests
import redis
import threading
from IndexTool import IndexTool
from futures_order_new import main, main_2


def data_redis(data):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    last_time = data['last_time']
    if not r.sismember('trans_set_new_5', last_time):
        data = json.dumps(data)
        r.lpush('trans_new_5', data)
        r.sadd('trans_set_new_5', last_time)


def setting_data_get():
    """
    获取配置信息
    :return: 
    """
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    data = r.hget('setting_data', 'lvjian')
    data = json.loads(data.decode())
    print(type(data), data)

    return data


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
        self.type = '3min'
        self.ma = [7, 30]
        self.buy_time = 0

    def signal(self):
        it = IndexTool()

        """
        kline数据获取
        """

        def data_kline_get():
            spot_url = 'https://www.okex.me/v2/spot/markets/kline?' \
                       'symbol=eos_usdt&type={}&limit=1000&coinVol=0'.format(self.type)
            futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                          'symbol=f_usd_eos&type={}&contractType=quarter&limit=1000&coinVol=1'.format(self.type)

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
        #last_price = futures_price()
        last_time = data_kline.index[-1]
        dif, dea, macd = it.MACD(data_kline)
        middle = round((data_kline.open + data_kline.close)/2, 3)
        #middle = data_kline.open
        macd *= 2
        x = 0.001

        num = 0
        is_buy = 0
        price = 0
        profit = 0
        profit_list = []
        for index, d in enumerate(list(zip(data_kline.index, macd, dif, middle, data_kline.high, data_kline.low, data_kline.close))):
            close_price = d[6]
            signal = ''
            signal_text = ''
            p = 0
            high, low = d[4], d[5]
            if index < 1:
                continue
            # if d[1]*macd[index-1] < 0 and abs(d[1]) > 0.001:
            #     signal = '++++++'
            #     num += 1
            if is_buy == 0:
                if d[1] > x and d[2] < 0:
                    print('开多')
                    signal_text = '开多'
                    is_buy = 1
                    price = d[3]
                    signal = '>>>>>>'
                elif d[1] < -x and d[2] > 0:
                    print('开空')
                    signal_text = '开空'
                    is_buy = -1
                    price = d[3]
                    signal = '<<<<<<'
            else:
                if d[1] > x and d[2] < 0 and is_buy == -1:
                    print('平空 开多')
                    signal_text = '平空 开多'
                    is_buy = 1
                    p = price - d[3]
                    profit += p
                    profit_list.append(p)
                    price = d[3]
                    signal = ('>>>>>>', p)
                elif d[1] < -x and d[2] > 0 and is_buy == 1:
                    print('平多 开空')
                    signal_text = '平多 开空'
                    is_buy = -1
                    p = d[3] - price
                    profit += p
                    profit_list.append(p)
                    price = d[3]
                    signal = ('<<<<<<', p)
            if signal:
                num += 1
            if p < 0:
                print('!'*100)
            ratio = 0
            if is_buy == 1:
                ratio = low - price
            elif is_buy == -1:
                ratio = price - high
            ratio = round(ratio, 3)
            lost = ''
            if ratio < -0.02:
                lost = '?'*30
            if last_time == d[0] and signal_text:
                if signal_text == '平空 开多':
                    main('4')
                    main('1')
                elif signal_text == '平多 开空':
                    main('3')
                    main('2')
                print('this is last time')
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
                data = {'last_time':last_time, 'updated_at':updated_at,
                        'price':close_price, 'signal_text':signal_text}
                data_redis(data)

            print(d, index, signal, ratio, lost)
        print(num, profit)
        profit_list = sorted(profit_list)
        print(profit_list)
        profit_list.pop(0)
        profit_list.pop(-1)
        print(sum(profit_list), profit_list)


if __name__ == '__main__':
    s = SIGNAL()
    t = threading.Thread(target=main_2)
    t.start()
    while True:
        try:
            setting_data = setting_data_get()
            is_host = setting_data.get('is_host')
            s.type = setting_data.get('type')
            ma1, ma2 = setting_data.get('ma1'), setting_data.get('ma2')
            print(is_host, s.type, ma1, ma2)
            if 0 < ma1 < ma2:
                s.ma = [ma1, ma2]
            s.signal()
            time.sleep(5)
        except Exception as e:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            error = {'last_time':time_now, 'error':str(e)}
            data_redis(error)
            time.sleep(5)
