import sys
sys.path.append('/root/exchange_new')
import json
import time
import random
import pandas as pd
import talib
from websocket import create_connection
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3, redis_4
import copy
from early_warning.symbol_remind import Remind


class RemindKline(Remind):

    redis_2 = redis_2

    def __init__(self):
        super().__init__()
        self.websocket_url = 'ws://47.52.115.31/v1/market/'
        self.send_data_day = {'market': '', 'method': 'kline', 'symbol': '',
                              'params': {'period': 86400, 'num': 200}, 'id': 1}
        #self.IS_TEST = True
        self.signal_match = {
            'signal_1':['UP_KDJ'], 'signal_2':['DOWN_KDJ'], # KDJ
            #'signal_3':['UP_LB','UP_BOLL','UP_VB'], # BOLL
            #'signal_4':['DOWN_LB','DOWN_BOLL','DOWN_VB'], # BOLL
            #'signal_5':['UP_SAR'], 'signal_6':['DOWN_SAR'], # SAR
            #'signal_7':['UP_MACD'], 'signal_8':['DOWN_MACD'], #MACD
        }

    def _remind_data_get(self):
        """
        获取用户订阅的提醒信息
        :return: 
        """
        data_obj = []
        try:
            sql = 'select *from uce_remind_kline where futures!=1'
            self.cursor.execute(sql)
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('kline指标监控 mysql数据获取异常:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('kline指标监控 mysql连接异常:{}'.format(e))
                    time.sleep(60*num)
                    num+=1
            time.sleep(5)

        remind_data = {}
        signal_dict = {}
        for signal_list in self.signal_match.values():
            for signal in signal_list:
                signal_dict[signal] = []
        for obj in data_obj:
            market = obj['platform'].lower()
            symbol = '{}_{}'.format(obj['symbol'],obj['currency'])
            user_id = obj['user_id']
            market_dict = remind_data.get(market)
            if market_dict:
                symbol_dict = market_dict.get(symbol)
                if not symbol_dict:
                    market_dict[symbol] = copy.deepcopy(signal_dict)
            else:
                remind_data[market] = {symbol:copy.deepcopy(signal_dict)}
            for signal_num,signal_list in self.signal_match.items():
                if obj.get(signal_num):
                    for signal in signal_list:
                        remind_data[market][symbol][signal].append(user_id)
        self.remind_data = remind_data

    def _kline_data_get(self, market, symbol):
        """
        获取kline数据
        :return: 
        """
        self.origin_data = []
        try:
            self.send_data_day['market'] = market
            self.send_data_day['symbol'] = symbol
            data_send = json.dumps(self.send_data_day)
            self.ws.send(data_send)
            data_recv = self.ws.recv()
            data = json.loads(data_recv)['data']
            if data:
                for d in data:
                    for i in range(1, 6):
                        d[i] = float(d[i])
                    d[0] = time.strftime('%Y-%m-%d %X',
                                         time.localtime(d[0] / 1000))
            self.origin_data = data
            dataFrame = pd.DataFrame(data,
                                     columns=['date', 'close', 'high', 'low',
                                              'open', 'volume'])
            dataFrame.index = dataFrame.date
            dataFrame = dataFrame.iloc[:, 1:]
            self.signal_data['last_time'] = dataFrame.index[-1]

            return dataFrame
        except Exception as e:
            logger.error('kline指标监控 {} {}kline数据获取异常{}'.format(
                market, symbol, e))
            while True:
                try:
                    self.ws = create_connection(self.websocket_url)
                    break
                except Exception as e:
                    logger.error('kline指标监控 {} {}websocket重连异常{}'.format(
                        market, symbol, e))
                    time.sleep(60)
            return

    def kdj_count(self, data):
        """
        KDJ指标计算
        :param data: 
        :return: 
        """
        try:
            data = self.origin_data
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
            text = None
            for r in result:
                signal = None
                k = r[-3]
                d = r[-2]
                if k < d and base == 1:
                    signal = 'DOWN_KDJ'
                    text = '{} {}日线KDJ指标出现死叉形态'
                    base = -1
                elif k > d and base == -1:
                    signal = 'UP_KDJ'
                    text = '{} {}日线KDJ指标出现金叉形态'
                    base = 1
            if signal:
                return signal, text
        except Exception as e:
            logger.error('kline指标监控 KDJ计算异常{}'.format(e))

    def boll_count(self, data):
        """
        BOLL指标计算
        :param data: 
        :return: 
        """
        try:
            VB, BOLL, LB = talib.BBANDS(data.close, timeperiod=20, nbdevup=2,
                                        nbdevdn=2, matype=0)
            open, close = data.open[-1], data.close[-1]
            signal, text = None, None
            if BOLL[-1] > close > LB[-1]:
                if open < LB[-1]:
                    signal = 'UP_LB'
                    text = '{} {}当前价格向上突破日线BOLL指标底线'
                elif open > BOLL[-1]:
                    signal = 'DOWN_BOLL'
                    text = '{} {}当前价格向下跌破日线BOLL指标中线'
            if VB[-1] > close > BOLL[-1]:
                if open < BOLL[-1]:
                    signal = 'UP_BOLL'
                    text = '{} {}当前价格向上突破日线BOLL指标中线'
                elif open > VB[-1]:
                    signal = 'DOWN_VB'
                    text = '{} {}当前价格向下跌破日线BOLL指标高线'
            if close > VB[-1] and open < VB[-1]:
                signal = 'UP_VB'
                text = '{} {}当前价格向上突破日线BOLL指标高线'
            elif close < LB[-1] and open > LB[-1]:
                signal = 'DOWN_LB'
                text = '{} {}当前价格向下跌破日线BOLL指标底线'
            if signal:
                return signal, text
        except Exception as e:
            logger.error('kline指标监控 BOLL计算异常{}'.format(e))

    def sar_count(self, data):
        """
        SAR指标计算
        :param data: 
        :return: 
        """
        try:
            SAR = talib.SAR(data.high, data.low, acceleration=0.027,
                                 maximum=0.19)
            signal, text = None, None
            shape = data.close - SAR
            if shape[-2] > 0 and shape[-1] < 0:
                signal = 'DOWN_SAR'
                text = '{} {}日线SAR指标出现下跌形态'
            elif shape[-2] < 0 and shape[-1] > 0:
                signal = 'UP_SAR'
                text = '{} {}日线SAR指标出现上涨形态'
            if signal:
                return signal, text
        except Exception as e:
            logger.error('kline指标监控 SAR计算异常{}'.format(e))

    def macd_count(self, data):
        """
        MACD指标计算
        :param data: 
        :return: 
        """
        try:
            DIF, DEA, MACD = talib.MACD(data.close, fastperiod=12, slowperiod=26,
                                        signalperiod=9)
            signal, text = None, None
            if MACD[-2] > 0 and MACD[-1] < 0:
                signal = 'DOWN_MACD'
                text = '{} {}日线MACD指标出现下跌形态'
            elif MACD[-2] < 0 and MACD[-1] > 0:
                signal = 'UP_MACD'
                text = '{} {}日线MACD指标出现上涨形态'
            if signal:
                return signal, text
        except Exception as e:
            logger.error('kline指标监控 MACD计算异常{}'.format(e))

    def index_commom(self, data):
        """
        执行指标计算
        :param data: 
        :return: 
        """
        index_list = [
            self.kdj_count,
            # self.boll_count,
            # self.sar_count,
            # self.macd_count,
            ]
        for index_cal in index_list:
            result = index_cal(data)
            if result:
                signal, text = result[0], result[1]
                self.signal_data['signal_list'].append(signal)
                self.signal_data[signal + '_DESC'] = text
                self.signal_data[signal + '_TIME'] = self.signal_data['last_time']

    def index(self):
        """
        指标
        :return: 
        """
        try:
            self.ws = create_connection(self.websocket_url)
        except Exception as e:
            logger.error('kline指标监控 websocket连接异常{}'.format(e))
            while True:
                try:
                    self.ws = create_connection(self.websocket_url)
                    break
                except Exception as e:
                    logger.error('kline指标监控 websocket重连异常{}'.format(e))
                    time.sleep(60)

        redis_data = self.redis_3.hgetall('remind_data_kline')
        self.redis_data = {k.decode(): json.loads(v.decode()) for k, v in
                            redis_data.items()} if redis_data else {}

        for market, symbols in self.remind_data.items():
            for symbol, users_dict in symbols.items():
                self.signal_data = {'signal_list': []}
                redis_key = market+'_'+symbol
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
                redis_value = self.redis_data.get(redis_key, {})
                kline_data = self._kline_data_get(market, symbol)
                if not isinstance(kline_data, pd.DataFrame):
                    continue
                self.index_commom(kline_data)
                for signal in self.signal_data['signal_list']:
                    signal_users = set(users_dict[signal])
                    redis_users = set(redis_value.get(signal, []))
                    time_name = signal + '_TIME'
                    text = self.signal_data[signal+'_DESC']
                    if self.signal_data[time_name] != redis_value.get(time_name):
                        need_send_users = signal_users
                    else:
                        need_send_users = signal_users - redis_users
                    for user in need_send_users:
                        message = text.format(market, symbol)
                        self._send_remind(message, market, symbol, user, True) #2019/1/7 改为生产
                redis_value.update(users_dict)
                redis_value.update(self.signal_data)
                redis_value['updated_at'] = updated_at
                self.redis_3.hset('remind_data_kline', redis_key, json.dumps(redis_value))
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
                self.index()
                time.sleep(1200)
            except Exception as e:
                logger.error('kline指标监控 主函数异常{}'.format(e))
                time.sleep(600)


if __name__ == '__main__':
    r = RemindKline()
    r.main()


