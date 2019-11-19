from test2_scrapy.test.talib_test.IndexTool import IndexTool
import talib

it = IndexTool()
it.kline_data_get(symbol='eos_usdt')
data = it.kline_data
print(data)

cci = talib.CCI(data.high, data.low, data.close, timeperiod=20)
print(cci)
for c in list(zip(cci.index, cci)):
    if c[-1] > 100 or c[-1] < -100:
        print(c)
