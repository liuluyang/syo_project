#import pymysql
#from test_scrapy.settings import MYSQL
from websocket import create_connection
import redis
import logging
import json
import time
import requests

class Gate(object):

    def __init__(self):
        self.num = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.markets = requests.get('https://data.gateio.io/api2/1/pairs').json()
        self.data_send = {"id":1, "method":"ticker.query", "params":["", 86400]}
        #m = requests.get('https://data.gateio.io/api2/1/pairs').json()
        try:
            self.pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
            self.redis = redis.Redis(connection_pool=self.pool)
            self.logger.info('已连接Redis服务：%s' % self.redis)
        except:
            self.logger.warning('Redis服务连接失败')
        self.ws = create_connection("wss://ws.gateio.io/v3/")
        pass

    def commit(self, data, market):
        self.redis.set(market, data)
        pass

    def revice(self):
        print ('开始。。。')
        while True:
            try:
                for market in self.markets[:10]:
                    print (self.ws)
                    self.data_send['params'] = [market,86400]
                    self.data_send = json.dumps(self.data_send)
                    print (self.data_send)
                    self.ws.send(self.data_send)
                    data_recv = self.ws.recv()
                    data_recv = json.loads(data_recv)
                    if not data_recv['error']:
                        result = data_recv['result']
                        result = json.dumps(result)
                        print (market, result)
                        self.commit(result, market)
                    time.sleep(0.05)
            except:
                self.ws = create_connection("wss://ws.gateio.io/v3/", timeout=20)
                self.logger.warning('websocket重新连接成功')
            time.sleep(10)

if __name__ == '__main__':
    g = Gate()
    g.revice()