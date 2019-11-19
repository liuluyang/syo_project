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
result = list(zip(data_kline.index, data_kline.low, data_sar, data_kline.close, data_kline.high, data_kline.close - data_sar))
#result_num = len(result)

up_num = 0
down_num = 0
# for r in result:
#     print(r)
#     if r[-1] > 0:
#         up_num +=1
#     elif r[-1] < 0:
#         down_num +=1
#
# print(up_num/result_num*100, down_num/result_num*100)
day_num = 0
profit = 0
x = 0
for r in result:
    if r[-1] < 0:
        if day_num == 0:
            low = r[1]
            print(r[1])
        day_num +=1
        print(r, low - r[2])
        x = low - r[2]
    elif r[-1] > 0:
        if day_num:
            print(r, '------------------------天数：', day_num, '回落：', r[-2] - r[-3])
            day_num = 0
            profit +=x
            print(x)

print(profit)


