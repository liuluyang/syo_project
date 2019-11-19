import talib
import numpy as np


import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

"""
SAR指标

"""

def kline_get():
    ws = create_connection('ws://47.52.115.31/v1/market/')
    d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':2000, 'period':3600*24},'id':1}
    d = json.dumps(d)
    ws.send(d)
    data_recv = ws.recv()
    data = json.loads(data_recv)['data']
    print(data)
    for d in data:
        for i in range(1, 5):
            d[i] = float(d[i])
        d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0]/1000))
    # data.append(['2018-12-14 00:00:00 T', 3500, 4025, 3245, 3500, '123'])
    # data.append(['2018-12-15 00:00:00 T', 3400, 3900, 3300, 3600, '123'])
    # data.append(['2018-12-16 00:00:00 T', 3400, 4000, 3600, 3700, '123'])

    dataFrame = pd.DataFrame(data, columns=['date', 'close', 'high', 'low', 'open', 'volume'])
    dataFrame.index = dataFrame.date
    dataFrame = dataFrame.iloc[:, 1:]
    #close = dataFrame.close

    return dataFrame

data = kline_get()
# data.high[-3] = 4080
# data.low[-3] = 3400
# data.low[-4] = 2400
real = talib.SAR(data.high, data.low, acceleration=0.02, maximum=0.2)
#print(real)

result = data.close - real
# for r in zip(result.index, result):
#     print(r)

for d in zip(data.index, data.high, data.low, real, result):
    print(d)




