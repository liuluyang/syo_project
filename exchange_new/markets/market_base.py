import json
import time
import requests
import threading
from queue import Queue

from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3


class MarketBase(object):
    name = None
    exchange_rate = {}
    exchange_rate_list = []
    change_info = {}

    logger = logger
    redis_2 = redis_2
    redis_3 = redis_3

    def __init__(self):
        self.market_name = '{name}_market'.format(name=self.name)
        self.exchange_rate_name = '{name}_exchange_rate'.format(name=self.name)
        self.ticker_name = '{name}_ticker'.format(name=self.name)
        self.ticker_name_new = '{name}_ticker_new'.format(name=self.name)

        self.is_break_len = len(self.exchange_rate_list)

    def market_update(self):
        """
        
        :return: True
        """
        pass

    def _market_get(self):
        """
        
        :return: {}
        """
        if not self.redis_2.exists(self.market_name):
            self.market_update()
        markets = self.redis_2.hgetall(self.market_name)
        markets_new = {}
        for k,v in markets.items():
            k, v = k.decode('utf8'), v.decode('utf8')
            markets_new[k] = v

        return markets_new

    def data_get(self):
        """
        
        :return: None
        """
        pass

    def _data_get_commom(self, thread_num=2):
        self.symbols = self._market_get()
        if thread_num<=0:
            thread_num = 2
        self.q = Queue()
        for i in range(thread_num):
            t = threading.Thread(target=self._data_send_new, args=(i,))
            t.start()
        t = threading.Thread(target=self._queue_counter)
        t.start()

    def _data_send_new(self, num):
        """
        最新价数据存入redis
        :return: 
        """
        while True:
            data = self.q.get()
            symbol, data = data['symbol'], data['data']
            #print('线程：{} 监测到数据'.format(num), symbol, data)
            data['updated_at'] = time.strftime('%Y-%m-%d %X',time.localtime())
            data = json.dumps(data)
            self.redis_3.hset(self.ticker_name, symbol, data)
            self.q.task_done()

    def _queue_counter(self):
        """
        管道计数器
        :return: 
        """
        while True:
            #print('{}管道队列剩余任务:'.format(self.ticker_name), self.q.qsize())
            warning_num = 1000
            q_num = self.q.qsize()
            if q_num >= warning_num:
                for i in range(warning_num):
                    self.q.get()
                    self.q.task_done()
                self.logger.warning('{}管道队列任务太多！{}'.
                                    format(self.ticker_name, q_num))
            time.sleep(2)

    def ticker_new(self):
        """
        
        :return: None
        """
        symbols = self._market_get()
        while True:
            try:
                self._exchange_rate_get()
                self._usd_update()
                logger.info('%s 更新完成'%(self.ticker_name_new))
                time.sleep(1)
            except Exception as e:
                logger.warning('%s 更新异常!!!! %s'%(self.ticker_name_new, e))
                time.sleep(5)

    def _exchange_rate_get(self):
        is_break = 0
        while True:
            for symbol in self.exchange_rate_list:
                data = self.redis_3.hget(self.ticker_name,
                                         self.redis_2.hget(self.market_name, symbol)
                                         )
                if data:
                    self.exchange_rate[symbol] = float(json.loads(data.decode())
                                                       [self.change_info['last']])
                    is_break+=1
            if is_break >= self.is_break_len:
                break
            else:
                is_break = 0
            time.sleep(1)
        try:
            data = requests.get('https://data.gateio.io/api2/1/ticker/usdt_cny', timeout=2)
            usd = float(data.json()['last'])
        except:
            exchange_rate = self.redis_2.get(self.exchange_rate_name)
            if exchange_rate:
                usd = float(json.loads(exchange_rate.decode())['USD'])
            else:
                usd = 7.0

        self.exchange_rate['USD'] = usd
        self.exchange_rate['updated_at'] = time.strftime('%Y-%m-%d %X',
                                                         time.localtime())
        self.redis_2.set(self.exchange_rate_name, json.dumps(self.exchange_rate))

    def _usd_update(self):
        symbols = self._market_get()
        mapping = {}
        for k_name, v_name in symbols.items():
            ticker_new = {'period':86400}
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            info = self.redis_3.hget(self.ticker_name, v_name)
            if not info:
                continue
            info = json.loads(info.decode())
            k_name_list = k_name.split('_')
            symbol, currency = k_name_list[0], k_name_list[1]

            ticker_new['updated_at'] = updated_at
            ticker_new['symbol'] = symbol
            ticker_new['currency'] = currency
            for k, v in self.change_info.items():
                ticker_new[k] = info.get(v, None)

            last_price = ticker_new['last']
            open_price = ticker_new['open']
            if last_price is None or open_price is None:
                continue
            last_price = float(last_price)
            open_price = float(open_price)

            rate = self.exchange_rate
            if currency=='USDT':
                ticker_new['usd_price'] = last_price
                ticker_new['cny_price'] = last_price*rate['USD']
                ticker_new['usd_open'] = open_price
            else:
                key = '_'.join([currency, 'USDT'])
                value = rate.get(key, None)
                if not value:
                    if self.name == 'zb' and currency == 'QC':
                        ticker_new['usd_price'] = last_price / rate['USD']
                        ticker_new['cny_price'] = last_price
                        ticker_new['usd_open'] = open_price / rate['USD']
                    else:
                        continue
                else:
                    ticker_new['usd_price'] = last_price*value
                    ticker_new['cny_price'] = last_price*value*rate['USD']
                    ticker_new['usd_open'] = open_price*value

            ticker_new = self._usd_update_other(ticker_new)
            ticker_new = json.dumps(ticker_new)
            mapping[k_name] = ticker_new

        self.redis_3.hmset(self.ticker_name_new, mapping)

    def _usd_update_other(self, ticker_new):
        """
        
        :param ticker_new: 
        :return:  ticker_new  type:{}
        """
        return ticker_new

    def symbols_get(self):
        """
        获取交易对
        :return: 
        """

    def symbols_check(self):
        """
        对比数据查看交易对是否有更新
        :return: 
        """
        self.mapping = {}
        self.symbols_get()
        symbols_new = set(self.mapping.keys())
        symbols_old = self.redis_2.hkeys(self.market_name)
        symbols_old = set([v.decode() for v in symbols_old])
        symbols_add = symbols_new - symbols_old
        symbols_remove = symbols_old - symbols_new
        print('交易所:', self.market_name)
        print('新:', len(symbols_new))
        print('旧:', len(symbols_old))
        print('新增:', symbols_add, len(symbols_add))
        print('下架:', symbols_remove, len(symbols_remove))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'*3)


