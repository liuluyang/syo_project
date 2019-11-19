import redis


pool = redis.ConnectionPool(host='47.52.115.31', port=6379, db=4, password='lvjian')
r = redis.Redis(connection_pool=pool)

huobi_times = r.hgetall('huobi_times')
symbols_times = set(huobi_times.keys())
print(symbols_times)
print(len(huobi_times), type(huobi_times))

huobi_kline = r.hgetall('huobi_kline')
symbols_kline = set(huobi_kline.keys())
print(symbols_kline)
print(len(huobi_kline), type(huobi_kline))

no_need = symbols_times-symbols_kline
print(len(no_need), no_need)