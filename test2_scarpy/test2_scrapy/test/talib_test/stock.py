
from test2_scrapy.test.talib_test.IndexTool import IndexTool
import requests
import json
import time
import pandas as pd

def stock(code=None):
    #date open close low high up percent volume amount
    #code = code
    pa = requests.get('http://www.szse.cn/api/market/ssjjhq/getHistoryData'
                      '?random=0.8339429993280651&cycleType=32&marketId=1&code={}'.format(code)).json()
    kline_data = pa['data']['picupdata']
    name = pa['data']['name']

    for d in kline_data:
        for i in range(1, 9):
            d[i] = float(d[i])

    dataFrame = pd.DataFrame(kline_data, columns=['date', 'open', 'close', 'low',
                                            'high', 'up', 'percent', 'volume', 'amount'])
    dataFrame.index = dataFrame.date
    dataFrame.index = pd.to_datetime(dataFrame.index, format='%Y-%m-%d')
    dataFrame = dataFrame.iloc[:, 1:]
    #print(dataFrame)

    it = IndexTool()
    sar = it.SAR(dataFrame)
    x = dataFrame.close - sar
    # for i in zip(dataFrame.index, x):
    #     print(i)

    kdj = it.KDJ_2(dataFrame)
    if x[-1] > 0 or kdj[0][-1] - kdj[1][-1] > 0:
        return name, code
    # for i in zip(dataFrame.index, kdj[0]):
    #     print(i)

    #it.matplot((dataFrame.close, 'close'), (sar, 'SAR'))

    #it.matplot((kdj[0], 'K'))

for i in range(1,100):
    time.sleep(0.5)
    code = str(i).rjust(6).replace(' ', '0')
    try:
        result = stock(code)
        if result:
            print(i, result)
        else:
            print(i, '-')
    except:
        pass

