import requests
import json
import threading
from queue import Queue
import time
import pymysql
from websocket import create_connection as create
from settings import MYSQL_PRO, MYSQL_TES, IS_TEST
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3, redis_4
from settings import Threshold_usd, IS_PUSH
import gzip
from early_warning.symbol_remind import Remind
import random


class TradeBase(object):
    redis_2 = redis_2
    redis_3 = redis_3
    redis_4 = redis_4

    def __init__(self):
        self.market = None
        self.IS_TEST = IS_TEST

    def mysql_obj_get(self):
        """
        连接数据库 并返回对象
        :return: 
        """
        MYSQL = MYSQL_TES if self.IS_TEST else MYSQL_PRO
        connect = pymysql.connect(**MYSQL)
        cursor = connect.cursor()

        return cursor, connect

    def mysql_save(self, data):
        """
        监测数据存入数据库
        :param data: 
        :param cursor: 
        :param connect: 
        :return: 
        """
        if not data:
            return
        cursor, connect = self.mysql_obj_get()
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        cursor.execute(
            """insert into uce_short_elves(market, symbol, currency, sym_cur, con_type,
                con, is_up, created_at, is_percent, is_amount, price, btc_num, con_id)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                self.market,
                data['symbol'],
                data['currency'],
                data['sym_cur'],
                data['con_type'],
                data['con'],
                data['is_up'],
                time_now,
                data['is_percent'],
                data['is_amount'],
                data['price'],
                data['btc_num'],
                data['con_id']
            )
        )
        connect.commit()
        connect.close()

    def tickers_get(self, market, update_time=5):
        """
        最新价获取 BTC价格获取
        :param market: 
        :return: 
        """
        self.tickers = {}
        while True:
            tickers = self.redis_3.hgetall('{}_ticker_new'.format(market))
            tickers = {k.decode(): json.loads(v.decode()) for k, v in
                       tickers.items()}
            exchange_rate = self.redis_2.get('{}_exchange_rate'.format(market))
            exchange_rate = json.loads(exchange_rate)

            self.tickers = tickers
            self.exchange_rate = exchange_rate
            time.sleep(update_time)

    def _data_compare(self, num):
        """
        数据计算比较
        :param num: 
        :return: 
        """
        while True:
            data = self.q.get()
            symbol, data = data['symbol'], data['data']
            if symbol in self.tickers:
                try:
                    btc_price = self.exchange_rate['BTC_USDT']
                    usd_price = self.tickers[symbol]['usd_price']
                    amount = float(data['amount'])
                    price = float(data['price'])
                    if symbol=='BTC_USDT':
                        trading_volume = price * amount
                    else:
                        trading_volume = usd_price * amount
                    if trading_volume >= Threshold_usd:
                        result = {}
                        is_buy = True if data['type'] == 'buy' else False
                        if is_buy:
                            result['con_type'], result['is_up'] = '大笔买入', 1
                            result['con_id'] = 7
                        else:
                            result['con_type'], result['is_up'] = '大笔卖出', 0
                            result['con_id'] = 8
                        result['symbol'], result['currency'] = symbol.split('_')
                        result['con'], result['sym_cur'] = trading_volume, symbol
                        result['is_percent'], result['is_amount'] = 0, 1
                        result['price'] = price
                        result['btc_num'] = amount if symbol=='BTC_USDT' else \
                            trading_volume/btc_price
                        t = threading.Thread(target=self.mysql_save, args=(result,))
                        t.start()
                        # 预警监控
                        if IS_PUSH:
                            data_remind = {'symbol':symbol,'signal_type':'signal_2',
                                           'data':result}
                            self.R.q_remind.put(data_remind)
                except Exception as e:
                    logger.warn(
                        '{} 子线程{} 数据处理异常{}'.format(self.market, num, e))

            self.q.task_done()

    def _common_one(self, thread_num):
        """
        公共初始化部分
        :param thread_num: 
        :return: 
        """
        self.trade_times = {}
        self.q = Queue()
        symbols = self.redis_2.hgetall('{}_market'.format(self.market))
        self.symbols = {k.decode(): v.decode() for k, v in symbols.items()}

        # 最新价获取 子线程
        t = threading.Thread(target=self.tickers_get, args=(self.market,))
        t.start()

        # 数据处理 子线程
        for i in range(thread_num):
            t = threading.Thread(target=self._data_compare, args=(i,))
            t.start()

        # 预警监控 子线程
        if IS_PUSH:
            self.R = Remind()
            self.R.main_2(self.market)

        # 数据获取 子线程
        self.trade_get()

    def _common_two(self):
        """
        交易记录计数器
        :return: 
        """
        while True:
            #print('{}交易次数记录：'.format(self.market), self.trade_times, len(self.trade_times))
            #print('{}管道队列剩余任务:'.format(self.market), self.q.qsize())
            warning_num = 1000
            q_num = self.q.qsize()
            if q_num >= warning_num:
                for i in range(warning_num):
                    self.q.get()
                    self.q.task_done()
                logger.warning('{} trade管道队列任务太多！{}'.format(self.market, q_num))
            time.sleep(1)

    def trade(self, thread_num=10):
        """
        主进程函数
        :param thread_num: 
        :return: None
        """
        self._common_one(thread_num)
        self._common_two()

    def trade_get(self):
        """
        启动trade线程
        :return: 
        """

    def trade_get_thread(self, k_name=None, v_name=None):
        """
        trade线程
        :return: 
        """

