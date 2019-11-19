import hmac
import base64
import requests
import json
import time
import redis
import copy
from test2_scrapy.test.talib_test.futures_account import FuturesAccount, redis_connection, profit_count

#用户信息
users_data = [
{'apiKey': '146537f4-7692-4821-ad5a-af03c8cca385',
'secretKey': '9681E893CC577593280A82FB43B3DD43',
'Passphrase':'lly123456', 'id':1},
]


def main_spot(user_data):
    """
    主函数(现货)
    :param user_data: 
    :return: 
    """
    r = redis_connection()    # 连接redis
    timestamp = time.time()
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    f = FuturesAccount(**user_data)
    f.spot_ticker_get()        # 现货价格
    f.spot_account_get()       # 现货账户信息
    spot_assets = {}           # 现货币种、数目、价值
    for currency, d in f.spot_account.items():
        equity = float(d['balance'])
        spot_assets[currency] = {'equity': equity,
                                    'value': f.spot_ticker.get(currency.upper(),
                                                               0) * equity}
        if currency == 'USDT':
            spot_assets[currency]['value'] = equity
    print(spot_assets)
    spot_currencies_old = r.hget('account', 'spot_currencies_' + f.id)
    spot_currencies_old = json.loads(
        spot_currencies_old.decode()) if spot_currencies_old else {}
    f.spot_account.update(spot_currencies_old)
    print(f.spot_account)
    # 现货总资产数目
    assets_all = round(sum([v['value'] for v in spot_assets.values()]), 2)
    print(assets_all)
    # 现货总资产配比
    match = []
    for k, v in spot_assets.items():
        v['currency'] = k
        v['percent'] = round(v['value'] / assets_all * 100, 2)
        match.append(v)
    match.sort(key=lambda x: x['percent'], reverse=True)
    print(match)
    # 当日现货总资产信息
    account_redis = r.hget('account', 'spot_account_' + f.id)
    account_redis = json.loads(account_redis.decode()) if account_redis else {}
    # 前一日现货总资产信息
    spot_profit = r.lindex('spot_profit_list_' + f.id, 0)
    spot_profit = json.loads(
        spot_profit.decode()) if spot_profit else {}
    # 初始化现货总资产信息
    spot_account = {'assets': assets_all, 'profit': 0, 'profit_percent': 0,
                       'out': 0, 'in': 0, 'change': 0, 'match': match,
                       'updated_at': time_now, 'timestamp': timestamp
                       }
    # 现货总流水账单
    spot_transfer = f.spot_account_ledger_get()
    ledger_ids = []
    for t in spot_transfer:
        print(t)
        if spot_profit and account_redis and \
                        t['timestamp'] > spot_profit['timestamp'] \
                and not r.sismember('spot_ledger_set_' + f.id, t['ledger_id']):
            amount = float(t['amount'])
            ledger_id = t['ledger_id']
            currency = t['currency'] if t.get('currency') else \
                t['instrument_id'].split('-')[0]
            price = f.spot_ticker.get(currency, 0)
            if amount > 0:
                account_redis['in'] += amount * price
            else:
                account_redis['out'] += amount * price
            ledger_ids.append(ledger_id)
    if account_redis and spot_profit:
        account_redis['timestamp'] = timestamp
        account_redis['updated_at'] = time_now
        account_redis['change'] = account_redis['out'] + account_redis['in']
        account_redis['match'] = match
        account_redis['assets'] = assets_all
        profit = assets_all - spot_profit['assets'] - account_redis['change']
        profit_percent = profit/(spot_profit['assets']+account_redis['in'])*100
        account_redis['profit'] = round(profit, 2)
        account_redis['profit_percent'] = round(profit_percent, 2)
    else:
        account_redis = spot_account
    if not spot_profit or account_redis['updated_at'].split(' ')[0] != \
        spot_profit['updated_at'].split(' ')[0]:
        r.lpush('spot_profit_list_'+f.id, json.dumps(account_redis))
        account_redis = spot_account
    if ledger_ids:
        r.sadd('spot_ledger_set_'+f.id, *ledger_ids)
    # 计算现货账户累计收益
    spot_profit_redis = r.lrange('spot_profit_list_' + f.id, 0, -1)
    spot_profit_redis = [json.loads(d.decode()) for d in
                            spot_profit_redis]
    spot_profit_redis.pop(-1)
    spot_profit_redis = [account_redis] + spot_profit_redis
    print(len(spot_profit_redis), spot_profit_redis)
    for num in [7, 30, -1]:
        result = profit_count(spot_profit_redis, num)
        account_redis.update(result)
    # 记录合约账户信息
    r.hset('account', 'spot_currencies_' + f.id, json.dumps(spot_assets))
    r.hset('account', 'spot_account_' + f.id, json.dumps(account_redis))
    print('当前现货账户信息：', account_redis)

    # 现货交易记录
    spot_orders = f.spot_orders_get()
    spot_orders.sort(key=lambda x: x['timestamp'], reverse=True)
    for o in spot_orders[::-1]:
        order_id = o['order_id']
        if not r.sismember('spot_order_set_' + f.id, order_id):
            r.lpush('spot_order_list_' + f.id, json.dumps(o))
            r.sadd('spot_order_set_' + f.id, order_id)
    print('当前现货账户交易记录：', spot_orders)

    print('#' * 30)


if __name__ == '__main__':
    main_spot(users_data[0])