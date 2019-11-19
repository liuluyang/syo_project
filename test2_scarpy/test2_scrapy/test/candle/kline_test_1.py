import tushare as ts
import matplotlib.pyplot as plt
import test2_scrapy.test.candle.mpl_finance as mpf
import numpy as np

from websocket import create_connection
import time
import json


ws = create_connection('ws://47.52.115.31/v1/market/')
d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':200, 'period':3600},'id':1}
d = json.dumps(d)
ws.send(d)
data_recv = ws.recv()
data_recv = json.loads(data_recv)
print(data_recv)
data = data_recv['data']
for d in data:
    for index in range(1, 5):
        d[index] = float(d[index])
print(data)

def candle(data=None):
    # data = ts.get_k_data('600519', ktype='D', autype='qfq', start='2017-09-17', end='')
    # print(data)
    # prices = data[['open', 'high', 'low', 'close']]
    # dates = data['date']
    # print(prices)
    # print(dates)
    # candleData = np.column_stack([list(range(len(dates))), prices])
    # print(type(candleData), candleData, len(candleData))
    candleData = data
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
    mpf.candlestick_ohlc(ax, candleData, width=0.5, colorup='r', colordown='b')
    plt.show()

candle(data)
