import time
import redis

def delete_db4():
    now = int(time.strftime('%H', time.localtime()))
    pool = redis.ConnectionPool(host='localhost', port=6379, db=4, password='lvjian')
    r = redis.Redis(connection_pool=pool)

    if now==0:
        r.delete('okex')
        r.delete('huobi')
    elif now==8:
        r.delete('gateio')
        r.delete('binance')


