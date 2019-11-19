import requests
import json, time
import redis

pool = redis.ConnectionPool(host='47.52.115.31', port=6379, db=2, password='lvjian')
r = redis.Redis(connection_pool=pool)

okex_symbols = r.hkeys('okex_market')
okex_symbols = set([k.decode() for k in okex_symbols])
print(okex_symbols)
print(len(okex_symbols))
#https://www.okex.me/api/spot/v3/instruments
symbols = requests.get('https://www.okex.me/api/spot/v3/instruments').json()
print(len(symbols))
for s in symbols:
    symbol = s.get('product_id')
    symbol = symbol.replace('-', '_')
    if symbol not in okex_symbols:
        print(symbol)

"""
BCH_BTC
BSV_BTC
HC_BTC
HC_ETH
BCH_USDT
BSV_USDT
HC_USDT
"""