from websocket import create_connection
import time
import json
import redis

pool = redis.ConnectionPool(host='47.75.223.85', port=6379, db=2, password='lvjian')
r = redis.Redis(connection_pool=pool)
symbols = r.hkeys('binance_market')
symbols = [s.decode() for s in symbols]

print (int(len(symbols)/10), symbols)

ws = create_connection('ws://47.52.115.31/v1/market/')

def data_get(num, d, s):
    ws.send(d)
    data_recv = ws.recv()
    data = json.loads(data_recv)
    print (num, data['data'], s)

d = {'market':'gateio','method':'kline','symbol':'HSR_USDT','params':{'period':3600*24, 'num':2},'id':1}
#d = json.dumps(d)
print(time.time())
for num, s in enumerate(symbols):
    d['symbol'] = s
    data_get(num, json.dumps(d), s)
print(time.time())