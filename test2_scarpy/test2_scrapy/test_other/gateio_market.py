
import redis
import requests
import json
from websocket import create_connection
import threading
import time
import logging
import asyncio



class Market(object):

    def __init__(self):
        #redis连接很快 获取交易所列表需要一秒
        #gateis接口连接需要时间几秒
        #print(time.time())
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        l = logging.FileHandler('market.log', 'a', encoding='utf8')
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        l.setFormatter(formatter)
        self.logger.addHandler(l)

        self.num = 0
        self.market_set = set()
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=2, password='lvjian')
        self.redis = redis.Redis(connection_pool=self.pool)

        self.pool_3 = redis.ConnectionPool(host='localhost', port=6379, db=3, password='lvjian')
        self.redis_3 = redis.Redis(connection_pool=self.pool_3)

        self.ws = create_connection("wss://ws.gateio.io/v3/")

    def market_update(self):

        markets = requests.get('https://data.gateio.io/api2/1/pairs').json()
        for market in markets:
            self.redis.sadd('gateio_market', market)
        self.logger.info('~~~~~~~交易对更新完成')

        return True

    def __market_get(self):
        #print (time.time())
        if not self.redis.exists('gateio_market'):
            self.market_update()
        markets = self.redis.smembers('gateio_market')
        markets = [m.decode('utf8') for m in markets]
        #print (markets)
        #print (time.time())
        return markets

    def date_get(self):
        markets = self.__market_get()
        market_num = len(markets)
        data_send_f = {'id':1, 'method':'ticker.query', 'params':None}
        while True:
            while True:
                try:
                    for market in markets:
                        data_send_f['params'] = [market, 86400]
                        data_send = json.dumps(data_send_f)
                        #print (type(data_send), data_send)
                        #if not self.redis_3.exists(market):
                        if market not in self.market_set:
                            t = threading.Thread(target=self.__date_send, args=(data_send,market))
                            t.start()
                        #self.date_send(data_send, market)
                        time.sleep(0.05)
                    if market_num==len(self.market_set):
                        self.market_set = set()
                        self.logger.info('~~~~~~~一次更新完成')
                        break
                except:
                    self.ws = create_connection("wss://ws.gateio.io/v3/")
                    self.logger.warning('websocket重新连接成功')
            time.sleep(5)

    def __date_send(self, data_send, market=None):
        self.ws.send(data_send)
        data_recv = self.ws.recv()
        data_recv = json.loads(data_recv)
        if not data_recv['error']:
            result = data_recv['result']
            result['updated_at'] = time.strftime('%Y-%m-%d %X', time.localtime())
            result = json.dumps(result)
            #print(result)
            self.redis_3.set(market, result)
            self.num+=1
            self.market_set.add(market)
            #print(self.num)


if __name__ == '__main__':
    m = Market()
    m.market_update()
    m.date_get()
