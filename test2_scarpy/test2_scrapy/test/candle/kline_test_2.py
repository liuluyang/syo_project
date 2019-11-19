import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from test2_scrapy.test.candle.mpl_finance import candlestick_ohlc

from websocket import create_connection
import time
import json
import datetime

ws = create_connection('ws://47.52.115.31/v1/market/')
d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':200, 'period':3600},'id':1}
d = json.dumps(d)
ws.send(d)
data_recv = ws.recv()
data_recv = json.loads(data_recv)
print(data_recv)
data = data_recv['data']
for d in data:
    for index in range(1, 5):
        d[index] = float(d[index])
    d[0] = d[0]/1000
    d[0] = date2num(datetime.datetime.fromtimestamp(d[0]))
    #d[0] = 737018.0
print(data)

def candle(data):
    ax = plt.subplot()
    mondays = WeekdayLocator(MONDAY)
    weekFormatter = DateFormatter('%y %b %d')
    ax.xaxis_date()
    # ax.xaxis.set_major_locator(mondays)
    # ax.xaxis.set_minor_locator(DayLocator())
    # ax.xaxis.set_major_formatter(weekFormatter)
    candlestick_ohlc(ax, data, width=0.017, colorup='r', colordown='g')
    ax.set_title('BTC_USDT')
    plt.xticks(rotation=50)
    #plt.setp(plt.gca().get_xticklabels(), rotation=50, horizontalalignment='center')
    plt.show()

candle(data)