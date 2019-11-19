import talib
import numpy as np
import pandas as pd
import json
import time
from websocket import create_connection
import requests
import redis
import threading


def data_kline_get(type='spot'):
    spot_url = 'https://www.okex.me/v2/spot/markets/kline?' \
               'symbol=eos_usdt&type=5min&limit=1000&coinVol=0'

    futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                  'symbol=f_usd_eos&type=5min&contractType=quarter&limit=1000&coinVol=1'

    url_dict = {'spot':spot_url, 'futures':futures_url}
    url_type = type
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

futures_data = data_kline_get('futures')
spot_data = data_kline_get('spot')[1000:]
# print(futures_data)
# print(spot_data)

for d in list(zip(spot_data.index, futures_data.close - spot_data.close)):
    signal = ''
    if d[-1] > 0:
        signal = '>>>>>>>>>'
    print(d, signal)


if __name__ == '__main__':
    pass