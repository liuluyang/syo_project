import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
from queue import Queue
import time
import pymysql
from websocket import create_connection as create
from settings import MYSQL_PRO, MYSQL_TES, IS_TEST, IS_PUSH
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3, redis_4
from early_warning.symbol_remind import Remind
import random
import gzip


class KlineBase(object):
    redis_2 = redis_2
    redis_3 = redis_3
    redis_4 = redis_4

    def __init__(self):
        self.websocket_url = 'ws://47.52.115.31/v1/market/'
        self.send_data_day = {'market': '', 'method': 'kline', 'symbol': '',
                              'params': {'period': 86400, 'num': 2}, 'id': 1}
        self.ws_num = 2
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

    def _mysql_save(self, data, cursor, connect):
        """
        监测数据存入数据库
        :param data: 
        :param cursor: 
        :param connect: 
        :return: 
        """
        if not data:
            return
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        cursor.execute(
            """insert into uce_short_elves(market, symbol, currency, sym_cur, con_type,
                con, is_up, created_at, is_percent, is_amount, con_id)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
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
                data['con_id']
            )
        )
        connect.commit()

    def _mysql_save_thread(self):
        """
        接收管道数据
        :return: 
        """
        cursor, connect = self.mysql_obj_get()
        while True:
            data = self.q.get()
            try:
                self._mysql_save(data, cursor, connect)
            except Exception as e:
                logger.warning('{} kline监控数据存储异常{}'.format(self.market,e))
                while True:
                    try:
                        connect.ping()
                        self._mysql_save(data, cursor, connect)
                        break
                    except Exception as e:
                        logger.warning(
                            '{} kline监控mysql连接异常{}'.format(self.market, e))
                        time.sleep(60)
            self.q.task_done()

    def kline_data_update(self, symbols):
        """
        redis db4  {market}_kline
        对交易对 yesterday_open yesterday_close today_open数据进行更新
        :return: 
        """
        not_updated = []
        market = self.market
        index = 0
        mapping = {}
        ws_list = [create(self.websocket_url) for i in range(self.ws_num)]
        self.send_data_day['market'] = market
        for sym in symbols:
            self.send_data_day['symbol'] = sym
            send_data = json.dumps(self.send_data_day)
            ws = ws_list[index]
            try:
                ws.send(send_data)
                data_recv = ws.recv()
            except Exception as e:
                logger.warning('kline_data_update websocket断开:{}'.format(market, e))
                ws_list[index] = create(self.websocket_url)
                ws = ws_list[index]
                ws.send(send_data)
                data_recv = ws.recv()
            data_recv = json.loads(data_recv)
            data = data_recv['data']
            index += 1
            if index == self.ws_num:
                index = 0
            if not data:
                not_updated.append(sym)
                continue
            r = {}
            r['updated_at'] = time.strftime('%Y-%m-%d %X',time.localtime())
            try:
                r['y_open'], r['y_close'] = float(data[-2][-2]), float(data[-2][1])
            except Exception as e:
                logger.warning('{}_kline {}日线数据缺失 {}'.format(market, sym, e))
                continue
            r['t_open'] = float(data[-1][-2])
            mapping[sym] = json.dumps(r)
            self.redis_4.hset('{}_kline'.format(market), sym, mapping[sym])
        #self.redis_4.hmset('{}_kline'.format(market), mapping)
        if len(not_updated) > 10:
            logger.warning('{}_kline redis数据更新未完成 {}'.format(market, ','.join(
                not_updated)))
            self.kline_data_update(not_updated)
        logger.info('{}_kline redis数据更新完成'.format(market))

    def _change_min_get(self):
        """
        获取基础校对数据 kline_base
        :return: 
        """
        symbols_num = len(self.symbols)
        kline_base = self.redis_4.hgetall('{}_kline'.format(self.market))
        times_check = self.redis_4.hgetall('{}_times'.format(self.market))

        if not kline_base:
            self.kline_data_update(self.symbols.keys())
            kline_base = self.redis_4.hgetall('{}_kline'.format(self.market))
            kline_base = {k.decode(): json.loads(v.decode()) for k, v in
                          kline_base.items()}
            self.kline_base = kline_base
        if not self.kline_base:
            kline_base = self.redis_4.hgetall('{}_kline'.format(self.market))
            kline_base = {k.decode(): json.loads(v.decode()) for k, v in
                          kline_base.items()}
            self.kline_base = kline_base

        if not times_check or symbols_num != len(times_check):
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            times_check = {
                k: {'up': 0, 'down': 0,
                    'up_base': self.kline_base[k]['t_open']*1.1 if self.kline_base.get(k) else 0,
                    'down_base': self.kline_base[k]['t_open']*0.9 if self.kline_base.get(k) else 0,
                    'updated_at': updated_at} for k in self.symbols.keys()}
            mapping = {k: json.dumps(v) for k, v in times_check.items()}
            self.redis_4.hmset('{}_times'.format(self.market), mapping)
            self.times_check = times_check
        if not self.times_check:
            times_check = {k.decode(): json.loads(v.decode()) for k, v in
                           times_check.items()}
            self.times_check = times_check

    def _change_min_loop(self):
        while True:
            self._change_min_get()
            time.sleep(60)

    def _common_one(self, thread_num):
        """
        公共初始化部分
        :param thread_num: 
        :return: 
        """
        self.times_check = {}  #盘中大涨大跌提醒次数检查
        self.kline_base = {}   #昨日开盘收盘
        self.q = Queue()
        symbols = self.redis_2.hgetall('{}_market'.format(self.market))
        self.symbols = {k.decode(): v.decode() for k, v in symbols.items()}
        self._change_min_get()

        # 获取基础校对数据 子线程
        t = threading.Thread(target=self._change_min_loop)
        t.start()

        # 数据处理 子线程
        for i in range(thread_num):
            t = threading.Thread(target=self._mysql_save_thread)
            t.start()

        # 预警监控 子线程
        if IS_PUSH:
            self.R = Remind()
            self.R.main_2(self.market)

        # 数据获取 子线程
        self.kline_get()

    def _common_two(self):
        """
        管道计数器
        :return: 
        """
        while True:
            #print('{}管道队列剩余任务:'.format(self.market), self.q.qsize())
            warning_num = 100
            q_num = self.q.qsize()
            if q_num >= warning_num:
                for i in range(warning_num):
                    self.q.get()
                    self.q.task_done()
                logger.warning('{} kline管道队列任务太多！{}'.format(self.market, q_num))
            time.sleep(1)

    def kline(self, thread_num=2):
        """
        主进程函数
        :return: 
        """
        self._common_one(thread_num)
        self._common_two()

    def _kline_get_thread(self, k_name, v_name):
        """
        获取kline_1m 子线程
        :param k_name: 
        :param v_name: 
        :return: 
        """
        kline1m_time = None
        kline5m_time = None
        kline_num = 0
        kline_data = []
        ws, data_send = self.websocket_send(k_name, v_name)

        while True:
            try:
                result = self.websocket_recv(ws)
                if not result:
                    continue
                open, close, kline_t = result

                kline_base = self.kline_base.get(k_name)

                if kline_base:
                    # 急速拉升、猛烈打压
                    if open != close and kline_t != kline1m_time:
                        result = {}
                        change_1m = (close-open)/open
                        if change_1m > 0.02 and open > kline_base['y_close']:
                            result['con_type'], result['is_up'] = '急速拉升', 1
                            result['con_id'] = 3
                        elif change_1m < -0.02 and open < kline_base['y_close']:
                            result['con_type'], result['is_up'] = '猛烈打压', 0
                            result['con_id'] = 4
                        if result:
                            result['symbol'], result['currency'] = k_name.split('_')
                            result['con'], result['sym_cur'] = change_1m*100, k_name
                            result['is_percent'], result['is_amount'] = 1, 0
                            kline1m_time = kline_t
                            self.q.put(result)
                            if IS_PUSH:#预警监控
                                data_remind = {'symbol': k_name,
                                               'signal_type': 'signal_3',
                                               'data': result}
                                self.R.q_remind.put(data_remind)
                            #print(result, kline_t, time.time()-kline_t/1000)

                    # 快速反弹、高台跳水
                    if kline_num != 5:
                        if not kline_data or kline_data[-1]['t'] != kline_t:
                            kline_num += 1
                            kline_data.append({'t':kline_t,'price':open})
                    else:
                        if kline_data[-1]['t'] != kline_t:
                            kline_data.pop(0)
                            kline_data.append({'t': kline_t, 'price': open})
                        if open != close and kline_t != kline5m_time:
                            result = {}
                            open_5m = kline_data[0]['price']
                            change_5m = (close-open_5m)/open_5m
                            if change_5m > 0.05 and open_5m < kline_base['y_close']\
                                and open_5m < kline_base['y_open']:
                                result['con_type'], result['is_up'] = '快速反弹', 1
                                result['con_id'] = 5
                            elif change_5m < -0.05 and open_5m > kline_base['y_close']\
                                and open_5m > kline_base['y_open']:
                                result['con_type'], result['is_up'] = '高台跳水', 0
                                result['con_id'] = 6
                            if result:
                                result['symbol'], result['currency'] = k_name.split('_')
                                result['con'], result['sym_cur'] = change_5m*100, k_name
                                result['is_percent'], result['is_amount'] = 1, 0
                                kline5m_time = kline_t
                                self.q.put(result)
                                if IS_PUSH:#预警监控
                                    data_remind = {'symbol': k_name,
                                                   'signal_type': 'signal_4',
                                                   'data': result}
                                    self.R.q_remind.put(data_remind)
                                #print(result, kline_t, time.time() - kline_t/1000)

                    # 盘中大涨、盘中大跌
                    result = {}
                    change_day = 0
                    times_check = self.times_check[k_name]
                    up_price = times_check['up_base']
                    down_price = times_check['down_base']
                    if open != close and close > up_price and up_price!=0:
                        result['con_type'], result['is_up'] = '盘中大涨', 1
                        result['con_id'] = 1
                        up_price = 1.05*close
                        t_open = kline_base['t_open']
                        change_day = (close - t_open) / t_open
                        times_check['up'] += 1
                        times_check['up_base'] = up_price
                    elif open != close and close < down_price and down_price!=0:
                        result['con_type'], result['is_up'] = '盘中大跌', 0
                        result['con_id'] = 2
                        down_price = 0.95*close
                        t_open = kline_base['t_open']
                        change_day = (close - t_open) / t_open
                        times_check['down'] += 1
                        times_check['down_base'] = down_price
                    if result:
                        result['symbol'], result['currency'] = k_name.split('_')
                        result['con'], result['sym_cur'] = change_day*100, k_name
                        result['is_percent'], result['is_amount'] = 1, 0
                        #self.abnormal_data(close, t_open, change_day, result)
                        self.redis_4.hset('{}_times'.format(self.market),k_name,
                                          json.dumps(times_check))
                        self.q.put(result)
                        if IS_PUSH:#预警监控
                            data_remind = {'symbol': k_name,
                                           'signal_type': 'signal_1',
                                           'data': result}
                            self.R.q_remind.put(data_remind)
                        #print(result, kline_t, time.time() - kline_t/1000)

            except Exception as e:
                logger.warn('{} {} 最新kline_1m获取异常{}'.format(self.market, k_name, e))
                while True:
                    try:
                        time.sleep(random.random())
                        ws = self.websocket_reconnection(data_send, k_name)
                        break
                    except Exception as e:
                        logger.warn(
                            '{} {} kline websocket异常{}'.format(self.market, k_name, e))
                        time.sleep(1)

    def kline_get(self):
        """
        启动kline数据获取线程
        :return: 
        """

    def websocket_send(self, k_name, v_name):
        """
        websocket连接
        :param k_name: 
        :param v_name: 
        :return: ws, data_send
        """

    def websocket_recv(self, ws):
        """
        websocket数据接收处理
        :param ws: 
        :return: open, close, kline_t or False
        """

    def websocket_reconnection(self, data_send, k_name):
        """
        websocket重连
        :param data_send: 
        :return: ws
        """

    def abnormal_data(self, close, open, change, result):
        """
        捕获bigone bibox异常数据
        :param close: 
        :param open: 
        :param change: 
        :param result: 
        :return:
        """
        try:
            if self.market in ('bigone','bibox','zb'):
                time_now = time.strftime('%Y-%m-%d %X', time.localtime())
                results = {'close':close, 'open':open, 'change':change, 'result':result}
                results['time'] = time_now
                self.redis_4.lpush('kline_abnormal_data', json.dumps(results))
        except:
            pass
