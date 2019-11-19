import redis
import time
import json
import pymysql

MYSQL = {'host':'47.75.223.85', 'port':3306, 'db':'lvjian', 'user':'root',
          'passwd':'lvjian', 'use_unicode':True}

class Notification(object):

    def __init__(self):
        self.market_list = ['gateio', 'binance', 'okex', 'huobi']
        self.up_init = 10
        self.down_init = -10
        pool_3 = redis.ConnectionPool(host='47.75.223.85', port=6379, db=3,
                                      password='lvjian')
        self.redis_3 = redis.Redis(connection_pool=pool_3)
        pool_4 = redis.ConnectionPool(host='47.75.223.85', port=6379, db=4,
                                      password='lvjian')
        self.redis_4 = redis.Redis(connection_pool=pool_4)
        self.connect = pymysql.connect(**MYSQL)
        self.cursor = self.connect.cursor()



    def change_day(self):

        times_check = self.redis_4.hgetall('gateio')
        if times_check:
            times_check = {k.decode():json.loads(v.decode()) for k,v in times_check.items()}
        else:
            times_check = {k.decode():{'up':0,'down':0,'up_base':self.up_init,'down_base':self.down_init}
                           for k in self.redis_3.hkeys('gateio_ticker_new')}
            mapping = {k:json.dumps(v) for k,v in times_check.items()}
            self.redis_4.hmset('gateio', mapping)
        print (times_check)

        result = []
        data = self.redis_3.hgetall('gateio_ticker_new')
        for k, v in data.items():
            k, v = k.decode(), json.loads(v.decode())
            change = float(v['change'])
            if change >= self.up_init:
                if times_check[k]['up']==0 or (times_check[k]['up']!=0 and change >=
                        times_check[k]['up_base']+5):
                    result.append(v)
                    times_check[k]['up'] += 1
                    times_check[k]['up_base'] = change
            elif change <= self.down_init:
                if times_check[k]['down']==0 or (times_check[k]['down']!=0 and change <=
                        times_check[k]['down_base']-5):
                    result.append(v)
                    times_check[k]['down'] += 1
                    times_check[k]['down_base'] = change
        print (times_check)
        print (result)

    def _change_day_get(self, market):
        times_check = self.redis_4.hgetall(market)
        if times_check:
            times_check = {k.decode(): json.loads(v.decode()) for k, v in
                           times_check.items()}
        else:
            times_check = {
            k.decode(): {'up': 0, 'down': 0, 'up_base': self.up_init,
                         'down_base': self.down_init}
            for k in self.redis_3.hkeys('{}_ticker_new'.format(market))}
            mapping = {k: json.dumps(v) for k, v in times_check.items()}
            self.redis_4.hmset(market, mapping)

        result = []
        data = self.redis_3.hgetall('{}_ticker_new'.format(market))
        for k, v in data.items():
            k, v = k.decode(), json.loads(v.decode())
            change = float(v['change'])
            if change >= self.up_init:
                if times_check[k]['up'] == 0 or (
                        times_check[k]['up'] != 0 and change >=
                        times_check[k]['up_base'] + 5):
                    result.append(v)
                    times_check[k]['up'] += 1
                    times_check[k]['up_base'] = change
            elif change <= self.down_init:
                if times_check[k]['down'] == 0 or (
                        times_check[k]['down'] != 0 and change <=
                        times_check[k]['down_base'] - 5):
                    result.append(v)
                    times_check[k]['down'] += 1
                    times_check[k]['down_base'] = change

        return result, times_check

    def mysql_save(self, data, market):

        pass


if __name__ == '__main__':
    w = Notification()
    w.change_day()