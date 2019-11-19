import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

"""
布林道通道
0.05s
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

def boll(data, period=20):
    import math
    start = time.time()
    close = data.close
    BOLL = pd.Series(0.0, index=data.index)
    VB = pd.Series(0.0, index=data.index)
    LB = pd.Series(0.0, index=data.index)
    base = sum(close[:period])
    for i in range(period, len(data)):
        base = base + close[i] - close[i-period]
        boll = base / period
        BOLL[i] = boll
        vb = 0
        for c in close[i-period+1:i+1]:
            vb += (c-boll)**2
        a20 = math.sqrt(vb/period)*2
        VB[i] = boll + a20
        LB[i] = boll - a20
    result = list(zip(BOLL.index, VB, BOLL, LB, data.close))

    print('用时：{}s'.format(time.time() - start))
    return result


data = kline_get()

boll = boll(data, 20)
for b in boll[20:]:
    c = b[-1]
    if c >b [1]:
        print(b, '高')
    elif c < b[-2]:
        print(b, '低')

