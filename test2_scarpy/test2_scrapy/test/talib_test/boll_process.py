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

#data_kline.close[-1] = 3010

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
result = list(zip(BOLL.index, VB, BOLL, LB, data_kline.close))
result_num = len(result)

top_num = 0
bottom_num = 0
up_num = 0
down_num = 0
for b in result[20:]:
    if b[-1] >b [1]:
        print(b, '高')
        top_num +=1
    elif b[-1] < b[-2]:
        print(b, '低')
        bottom_num +=1
    elif b[-1] > b[2]:
        print(b, '涨势')
        up_num +=1
    elif b[-1] < b[2]:
        print(b, '跌势')
        down_num +=1

percent = (top_num+bottom_num)/result_num*100
print('异常数据占总数:{}% 高点:低点={}:1'.format(round(percent, 4),
                                          top_num/bottom_num))
print(up_num/result_num*100)
print(down_num/result_num*100)