import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

"""
用时0.1s
"""

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

def rsvCal(data, period=9):
    result = []
    K, D, J = 50, 50, 50
    high_list = data.high
    low_list = data.low
    close_list = data.close
    rsv = pd.Series(0.0, index=data.index)
    k = pd.Series(0.0, index=data.index)
    d = pd.Series(0.0, index=data.index)
    j = pd.Series(0.0, index=data.index)
    for i in range(period-1, len(data)):
        high = max(high_list[i-period+1:i+1])
        low = min(low_list[i-period+1:i+1])
        close = close_list[i]
        #rsv[i] = (close-low)/(high-low)*100
        RSV = (close-low)/(high-low)*100
        K = 2 / 3 * K + 1 / 3 * RSV
        D = 2 / 3 * D + 1 / 3 * K
        J = 3 * K - 2 * D
        rsv[i] = round(RSV, 2)
        k[i] = round(K, 2)
        d[i] = round(D, 2)
        j[i] = round(J, 2)
        result = list(zip(list(rsv.index), list(rsv), list(k), list(d), list(j)))

    return result

def kdj(data):
    start = time.time()
    rsv = rsvCal(data)
    print(rsv)
    print('用时：{}s'.format(time.time() - start))


data = kline_get()
kdj(data)

