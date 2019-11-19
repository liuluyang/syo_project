import sys
sys.path.append('/root/okex_futures_6')
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

#测试 RSI
def data_redis(data):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    last_time = data['last_time']
    if not r.sismember('trans_set_new_6', last_time):
        data = json.dumps(data)
        r.lpush('trans_new_6', data)
        r.sadd('trans_set_new_6', last_time)


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
        last_time = data_kline.index[-1]
        close_price = data_kline.close[-1]
        rsi = talib.RSI(data_kline.close, timeperiod=6)
        #print(rsi)

        print(last_time, rsi[-2], rsi[-1], close_price, self.is_buy)
        signal_dict = {'开多':'1', '开空':'2', '平多':'3', '平空':'4'}
        signal_text = ''
        if rsi[-2] < 15 and rsi[-1] > 30 and self.is_buy != 1:
            signal_text = '开多'
        elif rsi[-1] > 60 and self.is_buy == 1:
            signal_text = '平多'
        elif rsi[-2] > 85 and rsi[-1] < 80 and self.is_buy != -1:
            signal_text = '开空'
        elif rsi[-1] < 30 and self.is_buy == -1:
            signal_text = '平空'
        if last_time != self.buy_time and signal_text:
            if signal_text == '开多':
                self.is_buy = 1
            elif signal_text == '开空':
                self.is_buy = -1
            else:
                self.is_buy = 0
            self.buy_time = last_time
            main(signal_dict[signal_text])

            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            data = {'last_time':last_time, 'updated_at':updated_at,
                    'price':close_price, 'signal_text':signal_text}
            data_redis(data)


if __name__ == '__main__':
    s = SIGNAL()
    t = threading.Thread(target=main_2)
    t.start()
    while True:
        try:
            # setting_data = setting_data_get()
            # is_host = setting_data.get('is_host')
            # s.type = setting_data.get('type')
            # ma1, ma2 = setting_data.get('ma1'), setting_data.get('ma2')
            # print(is_host, s.type, ma1, ma2)
            # if 0 < ma1 < ma2:
            #     s.ma = [ma1, ma2]
            s.signal()
            time.sleep(3)
        except Exception as e:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            error = {'last_time':time_now, 'error':str(e)}
            data_redis(error)
            time.sleep(5)
