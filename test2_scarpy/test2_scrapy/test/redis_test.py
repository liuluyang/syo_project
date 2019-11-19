import redis
import time
# self.pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
# self.redis = redis.Redis(connection_pool=self.pool)
pool = redis.ConnectionPool(host='localhost', port=6379, db=1, password='lvjian')
r = redis.Redis(connection_pool=pool)

# while True:
#     time.sleep(10)
#     print (r.get('AE_BTC'))
#     break

print (r.ping())
# print (r.get('binance_exchange_rate'))
#r.delete('a')

r.hset('token_transaction', 'fakdkaknn312nkjnkjn12', 123213)

result = r.hget('token_transaction', 'fakdkaknn312nkjnkjn12')
num = 4
if not r.sismember('list_set', num):
    r.lpush('list', num)
    r.sadd('list_set', num)
print (result)
print (type(result))

result = float(result.decode())
print (type(result))