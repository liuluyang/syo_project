
from websocket import create_connection
import json
import time
import redis
import requests

def okex_kline_get(symbol, type, size=100):
    """
    symbol:ltc_usdt
    type:1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    size:default and max 2000
    :return: 
    """
    symbol = symbol.lower()
    url = 'https://www.okex.com/api/v1/kline.do?symbol={symbol}&type={type}&size={size}'
    url = url.format(symbol=symbol, type=type, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    new_result = []
    for r in data:
        new_result.append([r[0], r[4], r[2], r[3], r[1], r[5]])
    return new_result

class Trans(object):

    def __init__(self):
        self.symbols = 'btc,ltc,eth,etc,eos,xrp,btg'.upper().split(',')
        symbols = 'btc,ltc,eth,okb,etc,eos,xrp,' \
                  'aac,abt,ace,act,ada,ae,aidoc,' \
                  'ark,bcd,bchabc,bchsv,bec,bkx,bnt,' \
                  'btg,btm,cai,can,chat,cic,cmt,' \
                  'ctxc,cvc,cvt,dadi,dash,dcr,dgb'.upper().split(',')
        self.symbols = symbols
        self.last_price = None
        pass

    def redis_obj_get(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=10,
                                      password='lvjian')
        self.redis_10 = redis.Redis(connection_pool=pool)

    def ws_obj_get(self):
        self.ws = create_connection('ws://47.52.115.31/v1/market/')

    def kline_get(self, symbol, period):
        #print(symbol, period)
        # d = {'market': 'okex', 'method': 'kline', 'symbol': symbol,
        #      'params': {'num': 200, 'period': period}, 'id': 1}
        # d = json.dumps(d)
        # self.ws.send(d)
        # data_recv = self.ws.recv()
        # data = json.loads(data_recv)['data']
        data = okex_kline_get(symbol, period)
        #print(data)
        for d in data:
            for i in range(1, 5):
                d[i] = float(d[i])
            d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0] / 1000))
        self.last_price = data[-1][1]

        return data

    def kdj_count(self, data):
        high_list, low_list = [], []
        for d in data[0:9]:
            high_list.append(d[2])
            low_list.append(d[3])
        high, low, close = max(high_list), min(low_list), data[8][1]
        K, D, J = 50, 50, 50
        rsv1 = (close - low) / (high - low) * 100
        result = [[data[8][0], rsv1, K, D, J]]
        for d in data[9:]:
            high_list.pop(0)
            high_list.append(d[2])
            low_list.pop(0)
            low_list.append(d[3])
            high = max(high_list)
            low = min(low_list)
            close = d[1]
            rsv1 = (close - low) / (high - low) * 100
            K = 2 / 3 * K + 1 / 3 * rsv1
            D = 2 / 3 * D + 1 / 3 * K
            J = 3 * K - 2 * D
            result.append(
                [d[0], round(rsv1, 2), round(K, 2), round(D, 2), round(J, 2)])
        #print(result[-1][2] > result[-1][3])

        return result[-1]

    def transaction(self, symbol):
        updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
        base_account = {'cash':0, 'quantity':0, 'is_buy':0, 'is_sell':0,
                        'has_buy':0, 'has_sell':0, 'updated_at':updated_at,
                        'last_price': None, 'profit':0
                        }
        base_recording = {
            'symbol':symbol,
            'cash':0, 'quantity':0, 'last_price':None, 'buy_price':None,
            'sell_price':None, 'profit':0, 'created_at':updated_at
        }
        account_data = self.redis_10.hget('Account', symbol)
        account_data = json.loads(
            account_data.decode()) if account_data else base_account
        kdj = []
        periods = ['1day', '12hour', '6hour']
        for period in periods:
            kdj.append(self.kdj_count(self.kline_get(symbol, period)))
        day, h12, h6 = kdj
        print(symbol, day[2] > day[3], h12[2] > h12[3], h6[2] > h6[3])
        trans_type = None
        trans_price = None
        other = None
        if day[2] > day[3]:#gold
            if h12[2] > h12[3] and h6[2] > h6[3]:#glod
                if not account_data['has_buy'] and account_data['is_buy']==1:
                    #buy
                    account_data['is_buy'] = 0
                    account_data['has_buy'] = 1
                    account_data['has_sell'] = 0
                    account_data['quantity'] += 100/self.last_price
                    account_data['cash'] -= 100
                    trans_type = 'buy'
                    trans_price = self.last_price
                    other = '12/6'
                elif not account_data['has_buy'] and account_data['is_buy'] == 0:
                    #wait buy
                    account_data['is_buy'] = 1
            if h12[2] < h12[3] and h6[2] < h6[3]:#death
                if not account_data['has_sell'] and account_data['is_sell']==1:
                    #sell
                    account_data['is_sell'] = 0
                    account_data['has_sell'] = 1
                    account_data['has_buy'] = 0
                    account_data['cash'] += account_data['quantity']*self.last_price
                    account_data['quantity'] = 0
                    trans_type = 'sell'
                    trans_price = self.last_price
                    other = '12/6'
                elif not account_data['has_sell'] and account_data['is_sell'] == 0:
                    #wait sell
                    account_data['is_sell'] = 1
        elif day[2] < day[3]:#death
            if not account_data['has_sell'] and account_data['is_sell'] == 1:
                # sell
                account_data['is_sell'] = 0
                account_data['has_sell'] = 1
                account_data['has_buy'] = 0
                account_data['cash'] += account_data[
                                            'quantity'] * self.last_price
                account_data['quantity'] = 0
                trans_type = 'sell'
                trans_price = self.last_price
                other = '24'
            elif not account_data['has_sell'] and account_data['is_sell'] == 0:
                # wait sell
                account_data['is_sell'] = 1

        history = {
            'symbol':symbol, 'trans_price':trans_price, 'trans_type':trans_type,
            'gold_day':day[2] > day[3],
            'gold_h12':h12[2] > h12[3],
            'gold_h6':h6[2] > h6[3],
            'profit':account_data['cash']+account_data['quantity']*self.last_price,
            'created_at':updated_at
        }
        self.redis_10.lpush('History', json.dumps(history))
        account_data['last_price'] = self.last_price
        account_data['profit'] = history['profit']
        account_data['updated_at'] = updated_at
        if trans_type:
            account_data['trans_price'] = trans_price
            account_data['trans_time'] = updated_at
        self.redis_10.hset('Account', symbol, json.dumps(account_data))

        if trans_type:
            recording = {
                'symbol': symbol, 'trans_price': trans_price,
                'trans_type': trans_type, 'cash':account_data['cash'],
                'quantity':account_data['quantity'],
                'profit':account_data['profit'],
                'other':other, 'created_at':updated_at
            }
            self.redis_10.lpush('Recording', json.dumps(recording))

    def main(self):
        self.redis_obj_get()
        self.ws_obj_get()
        for symbol in self.symbols:
            try:
                self.transaction(symbol+'_USDT')
            except Exception as e:
                created_at = time.strftime('%Y-%m-%d %X', time.localtime())
                error = {
                    'created_at':created_at,
                    'symbol':symbol,
                    'error':e
                }
                self.redis_10.lpush('Error', json.dumps(error))
            time.sleep(1)

if __name__ == '__main__':
    t = Trans()
    print(t.symbols)
    t.main()