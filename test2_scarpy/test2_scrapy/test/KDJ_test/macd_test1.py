import numpy as np
from websocket import create_connection
import json
import time
import pandas as pd

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
dataFrame.index = dataFrame.iloc[:,0]
#dataFrame.index = dataFrame.index
dataFrame = dataFrame.iloc[:, 1:]
close = dataFrame.close

def smaCal(data, k):
    sma = pd.Series(0.0, index=data.index)
    for i in range(k-1, len(data.close)):
        sma[i] = sum(close[(i-4):(i+1)])/k

    return sma

sma = smaCal(dataFrame, 5)
#print(sma)

def wmaCal(data, weight):
    k = len(weight)
    arrWeight = np.array(weight)
    Wma = pd.Series(0.0, index=data.index)
    for i in range(k-1, len(data.index)):
        Wma[i] = sum(arrWeight*data[(i-k+1):(i+1)])

    return Wma

wma = wmaCal(close, [0.1, 0.15, 0.2, 0.25, 0.3])
#print(wma)

def ewmaCal(data, period=5, exponential=0.2):
    Ewma = pd.Series(0.0, index=data.index)
    Ewma[period-1] = np.mean(data[:period])
    for i in range(period, len(data)):
        Ewma[i] = exponential*data[i] + (1-exponential)*Ewma[i-1]

    return Ewma

ewma = ewmaCal(close, 5, 0.2)
#print(ewma)

def ewmaCal_2(data, period=5, exponential=0.2):
    # Ewma = pd.Series(0.0, index=data.index)
    # Ewma[period-1] = np.mean(data[:period])
    # for i in range(period, len(data)):
    #     Ewma[i] = exponential*data[i] + (1-exponential)*Ewma[period-1]


    num1 = sum([v[1] for v in data[0:period]])/period
    print(num1)
    num_base = num1
    result = [(data[period-1][0], num1)]
    for i in range(period, len(data)):
        n = data[i][1]*exponential + num_base*(1-exponential)
        r = (data[i][0], n)
        print(r)
        result.append(r)
        num_base = n

    return result

#t = ewmaCal_2(data)

DIF = ewmaCal(close, 12, 2/(1+12)) - ewmaCal(close, 26, 2/(1+26))
DEA = ewmaCal(DIF, 9, 2/(1+9))
MACD = (DIF - DEA)*2
#print(DIF)
print(DEA.tail(100))
print(MACD.tail(100))