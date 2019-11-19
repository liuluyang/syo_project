
num_1 = 1516.4546
num_2 = 0.0031231
num_3 = 1.1151

import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6379, db=3, password='lvjian')
redis_local = redis.Redis(connection_pool=pool)

gateio_tickers = redis_local.hgetall('huobi_ticker_new')


def price_parse(num):
    if num == 0:
        return num
    #是否负数
    is_negative = True if num < 0 else False
    num = abs(num)
    num_str = str(num)
    new_num = num
    if num >= 1:
        new_num = round(num, 2)
    elif num < 1:
        others = {'0', '.'}
        for index, s in enumerate(num_str):
            if s not in others:
                new_num = float(num_str[0:index+3])
                if new_num >= 1:
                    new_num = round(num, 6)
                break

    return new_num/-1 if is_negative else new_num

print(price_parse(num_2))

for ticket, info  in gateio_tickers.items():
    #print(ticket, info)
    info = json.loads(info.decode())
    change = float(info['change'])
    cny_price = float(info['cny_price'])
    print(ticket, '涨幅：', change, '价格：', cny_price)
    print(ticket, '涨幅：', price_parse(change), '价格：', price_parse(cny_price))
