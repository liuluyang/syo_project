import redis
import json

pool = redis.ConnectionPool(host='47.52.115.31', port=6379, db=3, password='lvjian')
r = redis.Redis(connection_pool=pool)
#print (r.hgetall('gateio_ticker_ne'), 'no')
data = r.hgetall('gateio_ticker_new')
print (b'BTC_USDT' in data)
print (data[b'BTC_USDT'])


for k,v in data.items():
    k,v = k.decode(), json.loads(v.decode())
    #print (k, v)
    change = float(v['change'])
    if change>=10:
        print (k, v)
