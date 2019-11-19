import sys
sys.path.append('/root/exchange_new')
import json
import threading
from queue import Queue
import time
import random
import pymysql
from websocket import create_connection
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3, redis_4

from early_warning.symbol_remind import Remind


class RemindKline(Remind):

    redis_2 = redis_2

    def __init__(self):
        super().__init__()
        self.websocket_url = 'ws://47.52.115.31/v1/market/'
        self.send_data_day = {'market': '', 'method': 'kline', 'symbol': '',
                              'params': {'period': 86400, 'num': 60}, 'id': 1}
        self.IS_TEST = True

    def _remind_data_get(self):
        """
        获取用户订阅KDJ提醒信息
        :return: 
        """
        data_obj = []
        try:
            sql = 'select *from uce_remind_kline where type="kdj" and signal_1=1 or signal_2=1'
            self.cursor.execute(sql)
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('预警监控mysql数据获取异常:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('预警监控mysql连接异常:{}'.format(e))
                    time.sleep(60*num)
                    num+=1
            time.sleep(5)

        remind_data = {}
        for obj in data_obj:
            market = obj['platform'].lower()
            symbol = '{}_{}'.format(obj['symbol'],obj['currency'])
            user_id = obj['user_id']
            signal_1 = obj['signal_1']
            signal_2 = obj['signal_2']
            market_dict = remind_data.get(market)
            if market_dict:
                symbol_dict = market_dict.get(symbol)
                if not symbol_dict:
                    market_dict[symbol] = {'gold':[], 'death':[]}
            else:
                remind_data[market] = {symbol:{'gold':[], 'death':[]}}
            if signal_1:
                remind_data[market][symbol]['gold'].append(user_id)
            if signal_2:
                remind_data[market][symbol]['death'].append(user_id)
        self.remind_data = remind_data
        print(remind_data)

    def _kline_data_get(self, market, symbol):
        """
        获取kline数据
        :return: 
        """
        try:
            self.send_data_day['market'] = market
            self.send_data_day['symbol'] = symbol
            data_send = json.dumps(self.send_data_day)
            self.ws.send(data_send)
            data_recv = self.ws.recv()
            data = json.loads(data_recv)['data']
            if data:
                for d in data:
                    for i in range(1, 5):
                        d[i] = float(d[i])

            return data
        except Exception as e:
            logger.error('KDJ监控 kline数据获取异常{}'.format(e))
            while True:
                try:
                    self.ws = create_connection(self.websocket_url)
                    break
                except Exception as e:
                    logger.error('KDJ监控 websocket重连异常{}'.format(e))
                    time.sleep(60)
            return

    def _kdj_count(self, kline_data):
        """
        KDJ指数计算
        :return: 
        """
        try:
            data = kline_data
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

            base = 1
            signal = None
            for r in result:
                signal = None
                k = r[-3]
                d = r[-2]
                if k < d and base == 1:
                    signal = '死叉'
                    base = -1
                elif k > d and base == -1:
                    signal = '金叉'
                    base = 1
            print(signal)
            return {'timestamp':result[-1][0], 'is_cross':signal}
        except Exception as e:
            logger.error('KDJ监控 kdj计算异常{}'.format(e))
            return

    def kdj(self):
        try:
            self.ws = create_connection(self.websocket_url)
        except Exception as e:
            logger.error('KDJ监控 websocket连接异常{}'.format(e))
            while True:
                try:
                    self.ws = create_connection(self.websocket_url)
                    break
                except Exception as e:
                    logger.error('KDJ监控 websocket重连异常{}'.format(e))
                    time.sleep(60)

        self.redis_data = {}
        redis_info = self.redis_3.hgetall('remind_data_kdj')
        if redis_info:
            self.redis_data = {k.decode(): json.loads(v.decode()) for k, v in
                               redis_info.items()}

        for market, symbols in self.remind_data.items():
            for symbol, ids in symbols.items():
                gold_ids = ids['gold']
                death_ids = ids['death']
                key = market+'_'+symbol
                remind_info = self.redis_data.get(key, {})
                gold_users = set(remind_info.get('gold_users', []))
                death_users = set(remind_info.get('death_users', []))
                kline_data = self._kline_data_get(market, symbol)
                if not kline_data:
                    continue
                kdj_data = self._kdj_count(kline_data)
                if not kdj_data:
                    continue
                is_cross = kdj_data.get('is_cross')
                timestamp = kdj_data.get('timestamp')
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
                gold_timestamp = 0
                death_timestamp = 0
                if is_cross == '金叉':
                    for user in gold_ids:
                        if timestamp != remind_info.get(
                                'gold_timestamp') or user not in gold_users:
                            message = '{} {}日线KDJ指标出现金叉'.format(market, symbol)
                            print(message, '发送给用户:', user)
                            # self._send_remind(message, market, symbol,
                            #                   user, False)
                    gold_timestamp = timestamp
                elif is_cross == '死叉':
                    for user in death_ids:
                        if timestamp != remind_info.get(
                                'death_timestamp') or user not in death_users:
                            message = '{} {}日线KDJ指标出现死叉'.format(market, symbol)
                            print(message, '发送给用户:', user)
                            # self._send_remind(message, market, symbol,
                            #                   user, False)
                    death_timestamp = timestamp
                redis_data = {
                    'gold_timestamp':gold_timestamp,
                    'death_timestamp':death_timestamp,
                    'gold_users':gold_ids, 'death_users':death_ids,
                    'updated_at':updated_at
                }
                self.redis_3.hset('remind_data_kdj', key, json.dumps(redis_data))
        self.ws.close()

    def main(self, sleep_time=5):
        """
        主函数
        :param sleep_time: 
        :return: 
        """
        while True:
            try:
                self.mysql_obj_get()
                self._remind_data_get()
                self._device_token_get()
                # 测试数据
                self.test_data_get()
                self.kdj()
                time.sleep(1800)
            except Exception as e:
                logger.error('KDJ监控 主函数异常{}'.format(e))
                time.sleep(600)

    def test_data_get(self):

        symbols = self.redis_2.hkeys('{}_market'.format('okex'))
        remind_data = {}
        for symbol in symbols[:10]:
            remind_data[symbol.decode()] = {'gold':[random.choice([11,22])],
                                            'death':[random.choice([33,44])]
                                            }

        self.remind_data = {'okex':remind_data}
        print(self.remind_data)


if __name__ == '__main__':
    r = RemindKline()
    r.main()
    #r.test_data_get()


