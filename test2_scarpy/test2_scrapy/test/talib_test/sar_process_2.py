import talib
import numpy as np
import pandas as pd
import json
import time
from websocket import create_connection
#from test2_scrapy.test.talib_test.base import data_kline_get
import requests

from test2_scrapy.test.talib_test.IndexTool import IndexTool

def signal():
    it = IndexTool()

    """
    kline数据获取
    """
    #data_kline = data_kline_get()
    start = time.time()

    def data_kline_get():
        spot_url = 'https://www.okex.me/v2/spot/markets/kline?' \
                   'symbol=eos_usdt&type=3min&limit=1000&coinVol=0'

        futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                      'symbol=f_usd_eos&type=3min&contractType=quarter&limit=1000&coinVol=1'

        url_dict = {'spot':spot_url, 'futures':futures_url}
        url_type = 'futures'
        data = requests.get(url_dict[url_type]).json()
        data = data['data']
        #print(data)
        position_dict = {0:'createdDate',1:'close',2:'high',3:'low',4:'open',5:'volume'}
        data_new = []
        if url_type == 'spot':
            for d in data:
                #print(d)
                d_new = []
                for i in range(0, 6):
                    d_new.append(float(d[position_dict[i]]))
                d_new[0] = time.strftime('%Y-%m-%d %X', time.localtime(d_new[0] / 1000))
                data_new.append(d_new)
        else:
            for d in data:
                d[1], d[4] = d[4], d[1]
                d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0] / 1000))
                data_new = data


        dataFrame = pd.DataFrame(data_new, columns=['date', 'close', 'high', 'low', 'open',
                                                'volume'])
        dataFrame.index = dataFrame.date
        dataFrame = dataFrame.iloc[:, 1:]
        #print(dataFrame)

        return dataFrame

    data_kline = data_kline_get()
    dif, dea, macd = it.MACD(data_kline)
    #print(macd)

    # ema7, ema30 = it.EMA(data_kline, [7, 30])
    # ema_x = ema7 - ema30
    #print(ema_x)

    # k, d = it.KDJ_2(data_kline)
    # kdj_x = k - d
    # #print(k , d, kdj_x)

    sar = it.SAR(data_kline)
    sar_x = data_kline.close - sar
    #print(sar, sar_x)

    ma5, ma10 = it.MA(data_kline, [5, 10])
    ma_x = ma5 - ma10

    signal = pd.Series(0.0, index=data_kline.index)
    for i in range(len(data_kline)):
        num = 0
        if dif[i] > 0:
            num += 1
        else:
            num -= 1
        if macd[i] > 0:
            num += 1
        else:
            num -= 1

        # if ema_x[i] > 0:
        #     num += 1
        # else:
        #     num -= 1
        if ma_x[i] > 0:
            num += 1
        else:
            num -= 1

        # if kdj_x[i] > 0:
        #     num += 1
        # else:
        #     num -= 1
        # if k[i] >= 78:
        #     num += 1
        # elif k[i] <= 22:
        #     num -= 1

        # if sar_x[i] > 0:
        #     num += 1
        # else:
        #     num -= 1
        signal[i] = num


    #print(signal)
    profit = 0
    is_buy = 0
    buy_price = 0
    profit_list = []

    # for date, sig, price in list(zip(signal.index, signal, data_kline.close))[100:]:
    #     print(date, sig, price)
    #     if is_buy == 0:
    #         if sig > 0:
    #             print('看多')
    #             is_buy = 1
    #             buy_price = price
    #         elif sig < 0:
    #             print('看空')
    #             is_buy = -1
    #             buy_price = price
    #     else:
    #         if sig >= 0 and is_buy == -1:
    #             print('平空')
    #             p = (buy_price - price)/buy_price
    #             profit_list.append(p)
    #             print(p*100)
    #             profit += p
    #             is_buy = 0
    #             buy_price = 0
    #         elif sig <=0 and is_buy == 1:
    #             print('平多')
    #             p = (price - buy_price)/price
    #             profit_list.append(p)
    #             print(p*100)
    #             profit += p
    #             is_buy = 0
    #             buy_price = 0
    #     if is_buy == 0:
    #         if sig > 0:
    #             print('看多')
    #             is_buy = 1
    #             buy_price = price
    #         elif sig < 0:
    #             print('看空')
    #             is_buy = -1
    #             buy_price = price
    #
    # print('收益：{}%'.format(profit*100))

    # date_ = signal.index[100:]
    # signal = signal[100:]
    # open = data_kline.close[100:]
    # for index, data in enumerate(list(zip(date_, signal, open))):
    #     date, sig, price = data
    #     print(data)
    #     sig_b = signal[index-1]
    #     if index == 0:
    #         continue
    #     if is_buy == 0:
    #         if sig > 0:
    #             print('看多')
    #             is_buy = 1
    #             buy_price = price
    #         elif sig < 0:
    #             print('看空')
    #             is_buy = -1
    #             buy_price = price
    #     else:
    #         if sig_b > 0 and sig <= 0:
    #             print('平多 开空')
    #             p = (price - buy_price) / price
    #             print(p*100)
    #             profit_list.append(p)
    #             profit += p
    #             is_buy = -1
    #             buy_price = price
    #         elif sig_b < 0 and sig >= 0:
    #             print('平空 开多')
    #             p = (buy_price - price) / buy_price
    #             print(p*100)
    #             profit_list.append(p)
    #             profit += p
    #             is_buy = 1
    #             buy_price = price
    #         elif sig_b == 0 and sig != 0:
    #             if sig > 0 and is_buy == -1:
    #                 print('平空 开多')
    #                 p = (buy_price - price) / buy_price
    #                 print(p * 100)
    #                 profit_list.append(p)
    #                 profit += p
    #                 is_buy = 1
    #                 buy_price = price
    #             elif sig < 0 and is_buy == 1:
    #                 print('平多 开空')
    #                 p = (price - buy_price) / price
    #                 print(p * 100)
    #                 profit_list.append(p)
    #                 profit += p
    #                 is_buy = -1
    #                 buy_price = price

    date_ = signal.index[100:]
    signal = signal[100:]
    open = data_kline.close[100:]
    for index, data in enumerate(list(zip(date_, signal, open))):
        date, sig, price = data
        print(data)
        sig_b = signal[index - 1]
        if index == 0:
            continue
        if is_buy == 0:
            if sig > 0:
                print('看多')
                is_buy = 1
                buy_price = price
            elif sig < 0:
                print('看空')
                is_buy = -1
                buy_price = price
        else:
            if is_buy==1 and sig_b > sig:
                print('平多 开空')
                p = (price - buy_price) / price
                print(p * 100)
                profit_list.append(p)
                profit += p
                is_buy = -1
                buy_price = price
            elif is_buy==-1 and sig_b < sig:
                print('平空 开多')
                p = (buy_price - price) / buy_price
                print(p * 100)
                profit_list.append(p)
                profit += p
                is_buy = 1
                buy_price = price

    # date_ = signal.index[100:]
    # signal = sar_x[100:]
    # open = data_kline.open[100:]
    # for index, data in enumerate(list(zip(date_, signal, open, sar[100:]))):
    #     date, sig, price, s = data
    #     print(data)
    #     sig_b = sar_x[index - 1]
    #     if index == 0:
    #         continue
    #     if is_buy == 0:
    #         if sig > 0 and sig_b < 0:
    #             print('看多')
    #             is_buy = 1
    #             buy_price = price
    #         elif sig < 0 and sig_b > 0:
    #             print('看空')
    #             is_buy = -1
    #             buy_price = price
    #     else:
    #         if is_buy == 1 and sig < 0:
    #             print('平多 开空')
    #             p = (price - buy_price) / price
    #             print(p * 100)
    #             profit_list.append(p)
    #             profit += p
    #             is_buy = -1
    #             buy_price = price
    #         elif is_buy == -1 and sig > 0:
    #             print('平空 开多')
    #             p = (buy_price - price) / buy_price
    #             print(p * 100)
    #             profit_list.append(p)
    #             profit += p
    #             is_buy = 1
    #             buy_price = price

    print('收益：{}%'.format(profit*100))
    print(profit_list)
    print(max(profit_list), min(profit_list), len(profit_list))
#
# """
# SAR
# 计算结果正常
# """
# data_sar = talib.SAR(data_kline.high, data_kline.low, acceleration=0.027, maximum=0.19)
# #print(data_sar)
# result = list(zip(data_kline.index, data_kline.low, data_sar, data_kline.close, data_kline.high, data_kline.close - data_sar))
# #result_num = len(result)
#
# up_num = 0
# down_num = 0
# # for r in result:
# #     print(r)
# #     if r[-1] > 0:
# #         up_num +=1
# #     elif r[-1] < 0:
# #         down_num +=1
# #
# # print(up_num/result_num*100, down_num/result_num*100)
# day_num = 0
# profit = 0
# x = 0
#
# for index, r in enumerate(result[1:]):
#     close, sar_1, sar_2 = r[-3], result[index][-1], r[-1]
#     #print(index, r)
#     if sar_1 < 0 and sar_2 > 0:
#         profit -= close
#         print(r, profit)
#         x +=1
#     elif sar_1 > 0 and sar_2 < 0:
#         if x != 0:
#             profit += close
#             print(r, profit)
#
#
# print(profit)

#it.matplot((sar, 'sar'), (data_kline.close, 'close'))

while True:
    signal()
    time.sleep(10)