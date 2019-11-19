
from websocket import create_connection
import time
import json
"""
KDJ指标计算
用时可忽略
"""
ws = create_connection('ws://47.52.115.31/v1/market/')
d = {'market':'okex','method':'kline','symbol':'BTC_USDT','params':{'num':200, 'period':3600*24},'id':1}
d = json.dumps(d)
ws.send(d)
data_recv = ws.recv()
data = json.loads(data_recv)['data']
for d in data:
    for i in range(1, 5):
        d[i] = float(d[i])
    #print(d)


def parse_time(data):
    timestract = time.localtime(data/1000)
    timestr = time.strftime('%Y-%m-%d %X', timestract)
    return timestr
start = time.time()
high_list, low_list = [], []
for d in data[0:9]:
    high_list.append(d[2])
    low_list.append(d[3])
high , low, close = max(high_list), min(low_list), data[8][1]
K, D ,J= 50, 50, 50
#print(high, low, close)
rsv1 = (close-low)/(high-low)*100
result = [[data[8][0], rsv1, K, D, J]]
#print(result)
for d in data[9:]:
    high_list.pop(0)
    high_list.append(d[2])
    low_list.pop(0)
    low_list.append(d[3])
    high = max(high_list)
    low = min(low_list)
    close = d[1]
    rsv1 = (close - low) / (high - low) * 100
    #print(rsv1)
    K = 2/3*K + 1/3*rsv1
    D = 2/3*D + 1/3*K
    J = 3*K - 2*D
    print(d[0], parse_time(d[0]), K)
    result.append([d[0], round(rsv1, 2), round(K, 2), round(D, 2), round(J, 2)])

base = 1
#print(result)
for r in result:
    signal = None
    buy_sell = None
    k = r[-3]
    d = r[-2]
    if k>= 80 or d >= 80:
        buy_sell = '超买'
    elif k<= 20 or d <= 20:
        buy_sell = '超卖'
    if k < d and base == 1:
        signal = '死叉'
        base = -1
    elif k > d and base == -1:
        signal = '金叉'
        base = 1
    print(parse_time(r[0]), r, signal, buy_sell)
print('用时：{}s'.format(time.time() - start))