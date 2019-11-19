import requests
import time

"""
季度溢价
"""

symbols = 'btc,ltc,eth,etc,bch,eos,xrp,btg'.split(',')
day_1, day_3, week_1 = ('30min', 48), ('2hour', 36), ('6hour', 28)
url_spot = 'https://www.okex.me/v2/market/index/kLine?' \
           'symbol=f_usd_{}&type={}&limit={}&coinVol=0'
url_future = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
              'symbol=f_usd_{}&type={}&limit={}&coinVol=1&contractType=quarter'

def f_s():
    for symbol in symbols:
        data_day1_s = requests.get(
            url_spot.format(symbol, day_1[0], day_1[1])).json()
        data_day3_s = requests.get(
            url_spot.format(symbol, day_3[0], day_3[1])).json()
        data_week1_s = requests.get(
            url_spot.format(symbol, week_1[0], week_1[1])).json()
        time.sleep(0.5)
        data_day1_f = requests.get(
            url_future.format(symbol, day_1[0], day_1[1])).json()
        data_day3_f = requests.get(
            url_future.format(symbol, day_3[0], day_3[1])).json()
        data_week1_f = requests.get(
            url_future.format(symbol, week_1[0], week_1[1])).json()
        time.sleep(0.5)
        print(symbol)
        print(data_day1_s)
        print(data_day1_f)
        print(data_day3_s)
        print(data_day3_f)
        print(data_week1_s)
        print(data_week1_f)

f_s()
