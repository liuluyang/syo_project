import sys
sys.path.append('/root/exchange_new')
import requests
import json
import threading
import time
import pymysql
from settings import ticker_new_list, MYSQL_PRO, MYSQL_TES, IS_TEST
from settings import binance_ticker_name_new
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3


class Update(object):

    def __init__(self):
        self.sleep_time = 1
        self.ticker_new_list = ticker_new_list

    def ticker_new_get(self):
        """    
        :return: {}
        """
        data_dict = {}

        for name in self.ticker_new_list:
            markets = redis_3.hgetall(name)
            markets_new = {}
            for k, v in markets.items():
                k, v = k.decode('utf8'), json.loads(v.decode('utf8'))
                markets_new[k] = v
            name = name.split('_')[0]
            data_dict[name] = markets_new

        data_dict = self.ticker_new_change(data_dict)

        return data_dict

    def ticker_new_change(self, data):
        """
        
        :param data: 
        :return: {}
        """
        #币安平台的BCC币种名称更换成BCH
        #binance BCC - BTC BNB ETH USDT ->BCH
        name_binance = binance_ticker_name_new.split('_')[0]
        need_change_binance = {'BCC_BTC':'BCH_BTC','BCC_BNB':'BCH_BNB',
                               'BCC_ETH':'BCH_ETH','BCC_USDT':'BCH_USDT'}
        for befor,after in need_change_binance.items():
            old_data = data.get(name_binance, {}).pop(befor, None)
            if old_data:
                old_data['symbol'] = after.split('_')[0]
                data[name_binance][after] = old_data

        return data

    def mysql_obj_get(self):
        MYSQL = MYSQL_TES if IS_TEST else MYSQL_PRO
        self.connect = pymysql.connect(**MYSQL)
        self.cursor = self.connect.cursor()

    def exchange_update(self):
        self.mysql_obj_get()

        while True:
            try:
                data_dict = self.ticker_new_get()
                for market, data in data_dict.items():
                    for k,v in data.items():
                        self._mysql_thread(market, k, v)
                self.connect.commit()
                logger.info('uce_exchange数据表一次更新完成 MYSQL')
                time.sleep(self.sleep_time)
            except Exception as e:
                logger.warning('uce_exchange数据表更新异常 MYSQL！！！{error}'.
                               format(error=e))
                while True:
                    try:
                        self.connect.ping()
                        logger.info('uce_exchange数据表更新 MYSQL重新连接成功')
                        break
                    except Exception as e:
                        logger.warning('uce_exchange数据表更新 MYSQL重新连接失败'
                                       '！！！{error}'.format(error=e))
                        time.sleep(5)

    def _mysql_thread(self, market, sym_cur, info):
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        sql = 'select id from uce_exchange where ' \
              'sym_cur="{sym_cur}" and market="{market}"'.format(sym_cur=sym_cur,
                                                               market=market)
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchone()

        is_has = False
        if data_obj:
            is_has = True
        if is_has:
            self.cursor.execute(
                """update uce_exchange set period=%s, open=%s,
                    close=%s, high=%s, low=%s, last=%s,
                    p_change=%s, quote_vol=%s, base_vol=%s,
                    updated_at=%s, time_now=%s, currency=%s, 
                    usd_price=%s, cny_price=%s, usd_open=%s where id=%s""",
                (
                    info['period'],
                    info['open'],
                    info['close'],
                    info['high'],
                    info['low'],
                    info['last'],
                    info['change'],
                    info['quoteVolume'],
                    info['baseVolume'],
                    info['updated_at'],
                    time_now,
                    info['currency'],
                    info['usd_price'],
                    info['cny_price'],
                    info['usd_open'],
                    data_obj[0],
                )
            )
        else:
            self.cursor.execute(
                """insert into uce_exchange(market, symbol, currency, period, open,
                    close, high, low, last, p_change, quote_vol, base_vol,
                    updated_at, time_now, sym_cur, usd_price, cny_price, usd_open)
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s)""",
                (
                    market,
                    info['symbol'],
                    info['currency'],
                    info['period'],
                    info['open'],
                    info['close'],
                    info['high'],
                    info['low'],
                    info['last'],
                    info['change'],
                    info['quoteVolume'],
                    info['baseVolume'],
                    info['updated_at'],
                    time_now,
                    sym_cur,
                    info['usd_price'],
                    info['cny_price'],
                    info['usd_open']
                )
            )

    def _usd_average_price(self):
        sql = 'SELECT symbol,AVG(usd_price) AS avg_price,AVG(p_change) AS avg_change ' \
              'FROM uce_exchange GROUP BY symbol ORDER BY avg_price DESC'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        for obj in data_obj:
            is_has = False
            symbol = obj[0]
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            sql = 'select id from uce_ranking where symbol="%s"'%(symbol)
            self.cursor.execute(sql)
            id_obj = self.cursor.fetchone()
            if id_obj:
                is_has = True
            if is_has:
                self.cursor.execute(
                    """
                    update uce_ranking set avg_price=%s, p_change=%s, updated_at=%s
                    where id=%s
                    """,
                    (
                        obj[1],
                        obj[2],
                        time_now,
                        id_obj[0]
                    )
                )
            else:
                self.cursor.execute(
                    """
                    insert into uce_ranking(symbol, avg_price, p_change, updated_at) 
                    value(%s, %s, %s, %s)
                    """,
                    (
                     symbol,
                     obj[1],
                     obj[2],
                     time_now
                    )
                )
        self.connect.commit()
        logger.info('uce_ranking均价更新完成')

    def _market_val_update(self):
        self.cursor.execute('update uce_ranking set market_val=avg_price*circulation where '
                       'circulation is not NULL')
        self.connect.commit()
        logger.info('uce_ranking市值更新完成')

    def _market_val_order(self):
        self.cursor.execute('select id,symbol from uce_ranking order by market_val desc')
        objs = self.cursor.fetchall()
        num = 0
        for obj in objs:
            num+=1
            id = obj[0]
            self.cursor.execute('update uce_ranking set order_val=%s where id=%s'%(num,id))
        self.connect.commit()
        logger.info('uce_ranking市值排序更新完成')

    def _max_quote_update(self):
        self.cursor.execute('select market,symbol,currency,sym_cur,quote_vol from '
                       '(select * from uce_exchange order by quote_vol desc ) '
                       'as b group by symbol')
        objs = self.cursor.fetchall()
        for obj in objs:
            symbol = obj[1]
            market = obj[0]
            currency = obj[2]
            sym_cur = obj[3]
            self.cursor.execute(
                """
                update uce_ranking set market=%s, currency=%s, sym_cur=%s WHERE 
                symbol=%s
                """,
                (
                    market, currency, sym_cur, symbol
                )
            )
        self.connect.commit()
        logger.info('uce_ranking获取最大交易量更新完成')

    def ranking_update(self):
        self.mysql_obj_get()
        while True:
            try:
                #均价更新1
                self._usd_average_price()
                #市值更新2
                self._market_val_update()
                #市值排序3
                self._market_val_order()
                #最大量获取4
                self._max_quote_update()
                logger.info('uce_ranking数据表一次更新完成 MYSQL')
                time.sleep(self.sleep_time)
            except Exception as e:
                logger.warning('uce_ranking数据表更新异常 MYSQL！！！{error}'.
                               format(error=e))
                while True:
                    try:
                        self.connect.ping()
                        logger.info('uce_ranking数据表更新 MYSQL重新连接成功')
                        break
                    except Exception as e:
                        logger.warning('uce_ranking数据表更新 MYSQL重新连接失败'
                                       '！！！{error}'.format(error=e))
                        time.sleep(5)

    def circulation_update(self):
        self.mysql_obj_get()
        sql = 'select id, symbol from uce_ranking'
        self.cursor.execute(sql)
        symbols = self.cursor.fetchall()

        for name in symbols:
            id = name[0]
            name = name[1]
            sql = 'select id,name,circulation from uce_coin where name="%s"'%(name)
            self.cursor.execute(sql)
            cir_obj = self.cursor.fetchone()
            circulation = cir_obj[2] if cir_obj else 0

            self.cursor.execute(
                """
                update uce_ranking set circulation=%s where symbol=%s
                """,
                (circulation, name)
            )
        self.connect.commit()
        logger.info('uce_ranking流通量更新完成 MYSQL')


if __name__ == '__main__':
    u = Update()
    #u.exchange_update()
    #u.ranking_update()
    # uce_ranking 表首次生成之后 需要流通量数据
    u.circulation_update()
    #u.mysql_obj_get()
    #u.ticker_new_get()

