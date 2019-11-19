import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd


def kline_get():
    ws = create_connection('ws://47.52.115.31/v1/market/')
    d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':200, 'period':3600*24},'id':1}
    d = json.dumps(d)
    ws.send(d)
    data_recv = ws.recv()
    data = json.loads(data_recv)['data']
    for d in data:
        for i in range(1, 5):
            d[i] = float(d[i])
        d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0]/1000))

    dataFrame = pd.DataFrame(data, columns=['date', 'close', 'high', 'low', 'open', 'volume'])
    dataFrame.index = dataFrame.date
    dataFrame = dataFrame.iloc[:, 1:]
    #close = dataFrame.close

    return dataFrame

def maCal(data, period=7):
    start = time.time()
    close = data.close
    ma = pd.Series(0.0, index=data.index)
    for i in range(period, len(data)):
        s = close[i-period+1:i+1]
        #print(s)
        ma[i] = sum(s)/period
    print('用时：{}s'.format(time.time() - start))
    return ma

def maCal_2(data, period=7):
    start = time.time()
    close = data.close
    ma = pd.Series(0.0, index=data.index)
    base = sum(close[:period])
    for i in range(period, len(data)):
        base = base + close[i] - close[i-period]
        #print(base)
        ma[i] = base / period
    print('用时：{}s'.format(time.time() - start))
    return ma

data = kline_get()
#print(data)
#ma = maCal(data, 90)
#print(ma)

ma_2 = maCal_2(data, 20)
print(ma_2)

