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


def maCal(data, period=2):
    ma = pd.Series(0.0, index=data.index)
    for i in range(period, len(data)):
        s = data[i-period:i]
        ma[i] = sum(s)/period
    return ma


change_oc = abs(round((data_kline.close-data_kline.open)/data_kline.open*100, 2))
change_oc_avg = round(maCal(change_oc), 2)
change_oc_avg_p = abs((change_oc_avg-change_oc)/change_oc)
change_hl = abs(round((data_kline.high-data_kline.low)/data_kline.low*100, 2))
x = abs(round(change_hl/change_oc, 2))
result = list(
    zip(data_kline.index, change_oc, change_hl, x, change_oc_avg, change_oc_avg_p)
)
for r in result:
    print(r)
    pass

print(sum(change_oc_avg_p))