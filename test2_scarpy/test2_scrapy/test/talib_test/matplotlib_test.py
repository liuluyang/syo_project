import talib
import numpy as np
import pandas as pd
import json
import time
import requests
from websocket import create_connection
from matplotlib import pyplot as plt
from test2_scrapy.test.talib_test.base import data_kline_get

"""
kline数据获取
"""
# data_kline = data_kline_get()
# start = time.time()

def okex_kline_get(symbol, type, size=100):
    """
    symbol:ltc_usdt
    type:1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    size:default and max 2000
    :return: 
    """
    symbol = symbol.lower()
    url = 'https://www.okex.com/api/v1/kline.do?symbol={symbol}&type={type}&size={size}'
    url = url.format(symbol=symbol, type=type, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    new_result = []
    for r in data:
        new_result.append([r[0], r[4], r[2], r[3], r[1], r[5]])

    for d in new_result:
        for i in range(1, 6):
            d[i] = float(d[i])
        d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0]/1000))

    dataFrame = pd.DataFrame(new_result, columns=['date', 'close', 'high', 'low', 'open', 'volume'])
    dataFrame.index = dataFrame.date
    dataFrame.index = pd.to_datetime(dataFrame.index)
    dataFrame = dataFrame.iloc[:, 1:]
    return dataFrame


data_kline = okex_kline_get('btc_usdt', '1day', 2000)
print(data_kline)
data_sar = talib.SAR(data_kline.high, data_kline.low, acceleration=0.02, maximum=0.2)
#plt.plot(data_kline.open, label='开盘价', marker='o', linewidth=1)
plt.plot(data_kline.close, label='收盘价')
plt.plot(data_sar, label='SAR')
plt.legend(loc='best')
plt.grid(True, axis='both')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('BTC_USDT 日线收盘价')
plt.show()