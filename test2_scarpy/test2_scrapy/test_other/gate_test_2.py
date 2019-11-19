import pymysql
from test_scrapy.settings import MYSQL
from websocket import create_connection
import logging
import json
import time

class Gate(object):

    def __init__(self):
        self.num = 0
        self.logger = logging.getLogger()
        try:
            self.connect = pymysql.connect(**MYSQL)
            self.cursor = self.connect.cursor()
            self.logger.info('已连接mysql服务')
        except:
            self.logger.warning('mysql服务连接失败')
        self.ws = create_connection("wss://ws.gateio.io/v3/")
        pass

    def commit(self, data):
        self.cursor.execute(
            """insert into uce_trade(data_id,time,price,amount,type) 
                value (%s, %s, %s, %s, %s)
            """,
            (
                data['id'],
                data['time'],
                data['price'],
                data['amount'],
                data['type']
            )
        )
        self.connect.commit()
        pass

    def revice(self):
        data_send = '{"id":1, "method":"trades.query", "params":["BTC_USDT", 1, 7938163]}'

        while True:
            try:
                self.ws.send(data_send)
                data_recv = self.ws.recv()
                data_recv = json.loads(data_recv)
                if not data_recv['error']:
                    for per in data_recv['result']:
                        self.num +=1
                        print(self.num,per)
                        self.commit(per)
                #raise
            except:
                self.ws = create_connection("wss://ws.gateio.io/v3/", timeout=20)
                data = {'id':11111,'time':'111111','price':'1','amount':'1','type':'1'}
                print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                self.commit(data)
            time.sleep(0.5)

        #self.logger.warning('获取数据失败')
        pass

if __name__ == '__main__':
    g = Gate()
    g.revice()