from test2_scrapy.test.talib_test.IndexTool import IndexTool


it = IndexTool()
it.kline_data_get(symbol='eos_usdt')
EMA = it.EMA()
print(EMA)
data = it.kline_data
#print(data)
avg = (data.open+data.close)/2
#print(avg)

x = avg - EMA
date_range = []
# for d in list(zip(x.index, x)):
#     if d[-1] > 0:
#         print(d)
#         date_range.append(d[0])
new_x = list(zip(x.index, x))
num = 0
# for i in range(1, len(new_x)-1):
#     # if new_x[i][-1]>0 and new_x[i-1][-1]<0 and new_x[i][-1]>=0.1:
#     #     print(new_x[i])
#     if new_x[i][-1] > 0.1:
#         print(new_x[i])
#         num += 1
# print(num)

#print(EMA)
#it.matplot((EMA, 'EMA'), (avg, 'avg'), date_range=date_range)

all_day = len(data)
print(all_day)
data_new = list(zip(data.index, EMA, data.open, data.high, data.close))

num_h = 0
num_c = 0
for d in data_new:
    ema = d[1]
    o = d[2]
    h = d[-2]
    c = d[-1]
    if o < ema and h > ema:
        print(d)
        num_h += 1
    if o < ema and h > ema and c > ema:
        #print(d)
        num_c += 1
print(num_h)
print(num_c)
print(num_c/num_h*100)