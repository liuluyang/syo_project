import talib
import numpy as np
import pandas as pd
import json
import time
from websocket import create_connection
from test2_scrapy.test.talib_test.base import data_kline_get

"""
kline数据获取
"""
data_kline = data_kline_get()
start = time.time()

"""
SAR
计算结果正常
"""
data_sar = talib.SAR(data_kline.high, data_kline.low, acceleration=0.027, maximum=0.19)
#print(data_sar)
print(data_kline.close - data_sar)

"""
KDJ
计算结果 有些偏差±1
"""
data_kdj = talib.STOCH(data_kline.high,data_kline.low,data_kline.close,
  fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)

#print(data_kdj[0])
x = data_kdj[0] - data_kdj[1]
# x = x - 1
# for d in zip(x.index, x):
#     if d[1] > 0:
#         print(d, '上升')
#     else:
#         print(d)

"""
RSI
计算结果正常
"""
data_rsi1 = talib.RSI(data_kline.close, timeperiod=6)
data_rsi2 = talib.RSI(data_kline.close, timeperiod=12)
data_rsi3 = talib.RSI(data_kline.close, timeperiod=24)
#print(data_rsi1)

"""
MACD
计算结果正常
"""
DIF, DEA, MACD = talib.MACD(data_kline.close, fastperiod=12, slowperiod=26,
                            signalperiod=9)
# print(DIF)
# print(DEA)
#print(MACD)
#print(talib.EMA(data_kline.close, timeperiod=6))

"""
BOLL
计算结果正常
"""
VB, BOLL, LB = talib.BBANDS(
                data_kline.close,
                timeperiod=20,
                # number of non-biased standard deviations from the mean
                nbdevup=2,
                nbdevdn=2,
                # Moving average type: simple moving average here
                matype=0)
# print(VB)
# print(BOLL)
# print(LB)
# print(data_kline)

"""
OBV
计算结果正常
"""
OBV = talib.OBV(data_kline.close, data_kline.volume)
#print(OBV)

"""
MTM
计算结果正常
"""
MTM = talib.MOM(data_kline.close, timeperiod=12)
MTMMA = talib.SMA(MTM, timeperiod=6)
# print(MTM)
# print(MTMMA)


print('用时：',time.time()-start)