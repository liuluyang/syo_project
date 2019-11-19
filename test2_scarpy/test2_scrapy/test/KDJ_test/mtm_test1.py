import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

"""
动量指标
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

def mtmCal(data, period=12):
    mtm = pd.Series(0.0, index=data.index)
    for i in range(period, len(data)):
        mtm[i] = data[i] - data[i-period]

    return mtm

def mtmmaCal(data, period=6):
    mtmma = pd.Series(0.0, index=data.index)
    for i in range(period, len(data)):
        mtmma[i] = sum(data[(i-period+1):(i+1)])/period

    return mtmma


data = kline_get()
mtm = mtmCal(data.close)
#print(mtm)
for m in zip(mtm.index, mtm):
    if m[-1]>=0 :
        print(m, '上升')
    else:
        print(m)
mtmma = mtmmaCal(mtm)
#print(mtmma)
for m in zip(mtmma.index, mtmma):
    if m[-1]>=0 :
        print(m, '上升')
    else:
        print(m)