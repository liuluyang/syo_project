
from websocket import create_connection
import time
import json
"""
obv指标计算

"""
ws = create_connection('ws://47.52.115.31/v1/market/')
d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':2000, 'period':3600*24},'id':1}
d = json.dumps(d)
ws.send(d)
data_recv = ws.recv()
data = json.loads(data_recv)['data']
for d in data:
    for i in range(1, 6):
        d[i] = float(d[i])

print(data)
print(len(data))
def parse_time(data):
    timestract = time.localtime(data/1000)
    timestr = time.strftime('%Y-%m-%d %X', timestract)
    return timestr

def obv(data):
    obv_base = 0
    result = []
    for d in data:
        if d[1] >= d[-2]:
            obv_base += d[-1]
        else:
            obv_base -= d[-1]
        result.append((d[0], obv_base))

    for d in result:
        print(parse_time(d[0]), d[-1])

    return result

data = obv(data)
def Obv_(data, period=30):

    obv_base = 0
    for d in data[:period]:
        if d[1] >= d[-2]:
            obv_base += d[-1]
        else:
            obv_base -= d[-1]
    result = [(data[period-1][0], obv_base)]
    for i in range(period,len(data)):
        d_new = data[i]
        if d_new[1] >= d_new[-2]:
            obv_base += d_new[-1]
        else:
            obv_base -= d_new[-1]
        d_old = data[i-period]
        if d_old[1] >= d_old[-2]:
            obv_base -= d_old[-1]
        else:
            obv_base += d_old[-1]
        result.append((d_new[0], obv_base))

    # for d in result:
    #     print(parse_time(d[0]), d[-1])

    return result

def maObv(data):
    amount_30 = sum([v[-1] for v in data[:30]])
    result = []
    for i in range(30, len(data)):
        amount_30 = amount_30+data[i][-1]-data[i-30][-1]
        r = (amount_30)/30
        result.append((data[i][0], r))

    for d in result:
        print(parse_time(d[0]), d[-1])

    return result

maObv(data)