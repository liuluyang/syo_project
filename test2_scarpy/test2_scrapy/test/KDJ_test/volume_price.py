import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

"""
量价
"""

def kline_get():
    ws = create_connection('ws://47.52.115.31/v1/market/')
    d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':200, 'period':3600*24},'id':1}
    d = json.dumps(d)
    ws.send(d)
    data_recv = ws.recv()
    data = json.loads(data_recv)['data']
    for d in data:
        for i in range(1, 6):
            d[i] = float(d[i])
        d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0]/1000))

    dataFrame = pd.DataFrame(data, columns=['date', 'close', 'high', 'low', 'open', 'volume'])
    dataFrame.index = dataFrame.date
    dataFrame = dataFrame.iloc[:, 1:]
    #close = dataFrame.close

    return dataFrame
data = kline_get()

def volsmaCal(data, period=5):
    start = time.time()
    volume = data.volume
    ma = pd.Series(0.0, index=data.index)
    for i in range(period, len(data)):
        s = volume[i-period+1:i+1]
        #print(s)
        ma[i] = sum(s)/period
    print('用时：{}s'.format(time.time() - start))
    return ma

v5 = volsmaCal(data)
v10 = volsmaCal(data, 10)
#print(v5)
#print(v10)
v = (v5+v10)/2
#print(v)
result= data.volume - v
for r in zip(result.index,result):
    print(r)