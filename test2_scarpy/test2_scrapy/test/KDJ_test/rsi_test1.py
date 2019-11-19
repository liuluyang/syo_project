

# data = [4461.4075, 4406.7303, 4372, 3883.6150, 3835.0021, 3779, 4249.2639, 4268.2720]
# up = 0
# down = 0
# start = 4461.4075
# for p in data[1:7]:
#     print(p)
#     diff = p-start
#     if diff > 0:
#         up += diff
#     else:
#         down += diff
#     start = p
#
# up , down = up/6, abs(down/6)
#
# rsi = up/(up+down)*100
# print(rsi)
#40.79 43.80

from websocket import create_connection
import time
import json
"""
RSI指标计算
"""
ws = create_connection('ws://47.52.115.31/v1/market/')
d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':8, 'period':3600*24},'id':1}
d = json.dumps(d)
ws.send(d)
data_recv = ws.recv()
data = json.loads(data_recv)['data']
for d in data:
    for i in range(1, 5):
        d[i] = float(d[i])
    print(d)

def parse_time(data):
    timestract = time.localtime(data/1000)
    timestr = time.strftime('%Y-%m-%d %X', timestract)
    return timestr

data_diff = [[parse_time(d[0]), d[1]-d[-2]] for d in data]
print(data_diff)
#start = data_diff[0][-1]
def rsi_6(k=6):
    up = 0
    down = 0
    for d in data_diff[:k]:
        d = d[-1]
        if d > 0:
            up += d
        else:
            down +=abs(d)
    # up = up/6
    # down = down/6
    # print(up/(up+down)*100, data_diff[5])
    result = []
    index = 0
    for d_ in data_diff[k:]:
        d = d_[-1]
        start = data_diff[index][-1]
        #print(start)
        if start > 0:
            up -= start
        else:
            down -= abs(start)
        if d > 0:
            up += d
        else:
            down +=abs(d)
        index += 1
        #print(index, up, down)
        rsi = (up/k)/(up/k+down/k)*100
        print(d_[0], rsi)
        #result.extend([d[0], rsi])

rsi_6()


cha = [data[i][1]-data[i-1][1] for i in range(1,len(data))][:-1]
print(cha)
up = sum([k for k in cha if k>=0])/6
down = sum([k for k in cha if k<0])/6
rsi1 = up/(up+abs(down))*100
print(rsi1)


