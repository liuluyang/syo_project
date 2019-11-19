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
import requests
from early_warning.symbol_remind import Remind


class RemindKline(Remind):

    redis_2 = redis_2

    def __init__(self):
        super().__init__()
        self.url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                   'symbol=f_usd_{}&type={}&contractType={}&limit=500&coinVol=1'
        self.contract_dict = {'this_week':'当周','next_week':'次周','quarter':'季度'}
        self.IS_TEST = True

    def _remind_data_get(self):
        """
        获取用户订阅的提醒信息(期货合约)
        :return: 
        """
        data_obj = []
        try:
            sql = 'select *from uce_remind_kline where futures=1'
            self.cursor.execute(sql)
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('kline-futures指标监控 mysql数据获取异常:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('kline-futures指标监控 mysql连接异常:{}'.format(e))
                    time.sleep(60*num)
                    num+=1
            time.sleep(5)

        remind_data = {}
        ks = set()
        for obj in data_obj:
            """
            OKEX-BTC-this_week-1hour-BOLL
            platform: OKEX
            symbol: EOS LTC BTC ETH ETC BTG XRP
            contract: this_week next_week quarter
            periods: 1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour day
            """
            market = obj['platform'].lower()
            symbol = '{}'.format(obj['symbol'])
            contract = obj['contract']
            type = obj['type']
            user_id = obj['user_id']
            params = obj['params']
            periods = []
            if params:
                try:
                    periods = json.loads(params)['periods']
                except Exception as e:
                    print(e)
            for period in periods:
                k = '{}-{}-{}-{}-{}'.format(market, symbol, contract, period,
                                            type).lower()
                k_p = '{}-{}-{}-{}'.format(market, symbol, contract, period).lower()
                ks.add(k_p)
                if k in remind_data:
                    remind_data[k].append(user_id)
                else:
                    remind_data[k] = [user_id]
        self.remind_data = remind_data
        self.ks = ks
        print(remind_data, ks)

    def _kline_data_get(self, k):
        """
        获取kline数据
        :return: 
        """
        time.sleep(0.5)
        self.origin_data = []
        market, symbol, contract, period = k.split('-')
        try:
            data = None
            if market == 'okex':
                data = requests.get(self.url.format(symbol, period, contract)).json()['data']
            if data:
                for d in data:
                    d[1], d[4] = d[4], d[1]
                    d[0] = time.strftime('%Y-%m-%d %X',
                                         time.localtime(d[0] / 1000))
            self.origin_data = data
            dataFrame = pd.DataFrame(data,
                                     columns=['date', 'close', 'high', 'low',
                                              'open', 'volume'])
            dataFrame.index = dataFrame.date
            dataFrame = dataFrame.iloc[:, 1:]
            self.signal_data['last_time'] = dataFrame.index[-1]
            self.price = dataFrame.close[-1]
            return dataFrame
        except Exception as e:
            logger.error('kline-futures指标监控 kline数据获取异常{} {}'.format(e, k))
            return

    def kdj_count(self, data, k):
        """
        KDJ指标计算
        :param data: 
        :return: 
        """
        k += '-kdj'
        try:
            data = self.origin_data
            high_list, low_list = [], []
            for d in data[0:9]:
                high_list.append(d[2])
                low_list.append(d[3])
            high, low, close = max(high_list), min(low_list), data[8][1]
            K, D, J = 50, 50, 50
            x = 1 if high - low == 0 else high - low
            rsv1 = (close - low) / x * 100
            result = [[data[8][0], rsv1, K, D, J]]
            for d in data[9:]:
                high_list.pop(0)
                high_list.append(d[2])
                low_list.pop(0)
                low_list.append(d[3])
                high = max(high_list)
                low = min(low_list)
                close = d[1]
                x = 1 if high - low == 0 else high - low
                rsv1 = (close - low) / x * 100
                K = 2 / 3 * K + 1 / 3 * rsv1
                D = 2 / 3 * D + 1 / 3 * K
                J = 3 * K - 2 * D
                result.append(
                    [d[0], round(rsv1, 2), round(K, 2), round(D, 2), round(J, 2)])

            signal, text = k, ''
            if result[-1][2] >= 80:
                text += '超买区'
            elif result[-1][2] <= 20:
                text += '超卖区'
            if result[-2][2] > result[-2][3] and result[-1][2] < result[-1][3]:
                text += ' 出现死叉形态'
            elif result[-2][2] < result[-2][3] and result[-1][2] > result[-1][3]:
                text += ' 出现金叉形态'
            if text:
                return signal, text
        except Exception as e:
            logger.error('kline-futures指标监控 KDJ计算异常{} {}'.format(e, k))

    def boll_count(self, data, k):
        """
        BOLL指标计算
        :param data: 
        :return: 
        """
        k += '-boll'
        try:
            VB, BOLL, LB = talib.BBANDS(data.close, timeperiod=20, nbdevup=2,
                                        nbdevdn=2, matype=0)
            open, close = data.open[-1], data.close[-1]
            signal, text = k, None
            if BOLL[-1] > close > LB[-1]:
                if open < LB[-1]:
                    text = '向上突破底线'
                elif open > BOLL[-1]:
                    text = '向下跌破中线'
            if VB[-1] > close > BOLL[-1]:
                if open < BOLL[-1]:
                    text = '向上突破中线'
                elif open > VB[-1]:
                    text = '向下跌破高线'
            if close > VB[-1] and open < VB[-1]:
                text = '向上突破高线'
            elif close < LB[-1] and open > LB[-1]:
                text = '向下跌破底线'
            if text:
                return signal, text
        except Exception as e:
            logger.error('kline-futures指标监控 BOLL计算异常{} {}'.format(e, k))

    def sar_count(self, data, k):
        """
        SAR指标计算
        :param data: 
        :return: 
        """
        k += '-sar'
        try:
            SAR = talib.SAR(data.high, data.low, acceleration=0.027,
                                 maximum=0.19)
            signal, text = k, None
            shape = data.close - SAR
            if shape[-2] > 0 and shape[-1] < 0:
                text = '出现下降形态'
            elif shape[-2] < 0 and shape[-1] > 0:
                text = '出现上升形态'
            if text:
                return signal, text
        except Exception as e:
            logger.error('kline-futures指标监控 SAR计算异常{} {}'.format(e, k))

    def macd_count(self, data, k):
        """
        MACD指标计算
        :param data: 
        :return: 
        """
        k += '-macd'
        try:
            DIF, DEA, MACD = talib.MACD(data.close, fastperiod=12, slowperiod=26,
                                        signalperiod=9)
            signal, text = k, ''
            position = DIF[-1] / self.price
            position_signal = ''
            if position >= 0.01:
                position_signal = '高位 '
            elif position <= -0.01:
                position_signal = '低位 '
            if MACD[-2] > 0 and MACD[-1] < 0:
                text += '出现死叉形态'
            elif MACD[-2] < 0 and MACD[-1] > 0:
                text += '出现金叉形态'
            if text:
                text = position_signal + text
                return signal, text
        except Exception as e:
            logger.error('kline-futures指标监控 MACD计算异常{} {}'.format(e, k))

    def index_commom(self, data, k):
        """
        执行指标计算
        :param data: 
        :return: 
        """
        index_list = [
            self.kdj_count,
            self.boll_count,
            self.sar_count,
            self.macd_count,
            ]
        for index_cal in index_list:
            result = index_cal(data, k)
            if result:
                signal, text = result[0], result[1]
                self.signal_data['signal_list'].append(signal)
                self.signal_data[signal + '_DESC'] = text
                self.signal_data[signal + '_TIME'] = self.signal_data['last_time']

    def index(self):
        """
        指标(期货合约)
        :return: 
        """
        redis_data = self.redis_3.hgetall('remind_data_kline_futures')
        self.redis_data = {k.decode(): json.loads(v.decode()) for k, v in
                            redis_data.items()} if redis_data else {}

        for k in self.ks:
            self.signal_data = {'signal_list': []}
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            redis_value = self.redis_data.get(k, {})
            kline_data = self._kline_data_get(k)
            if not isinstance(kline_data, pd.DataFrame):
                continue
            self.index_commom(kline_data, k)
            users_dict = {}
            print(self.signal_data)
            for signal in self.signal_data['signal_list']:
                market, symbol, contract, period, type = signal.split('-')
                signal_users = self.remind_data.get(signal, [])
                if signal_users:
                    users_dict[signal] = copy.deepcopy(signal_users)
                    signal_users = set(signal_users)
                else:
                    continue
                redis_users = set(redis_value.get(signal, []))
                time_name = signal + '_TIME'
                text = self.signal_data[signal+'_DESC']
                if self.signal_data[time_name] != redis_value.get(time_name):
                    need_send_users = signal_users
                else:
                    need_send_users = signal_users - redis_users
                symbol = symbol.upper()
                for user in need_send_users:
                    message = '[{} {} {}期货 {}线 {}指标],现价:{} {}'.\
                        format(market.upper(), symbol,
                               self.contract_dict[contract], period,
                               type.upper(), self.price, text
                               )
                    print(message, user)
                    symbol += '_USD'
                    self._send_remind(message, market, symbol, user, mode=False,
                                      message_type=3)
                    self.remind_history(user_id=user, content=message, type=2)
            self.connect.commit()
            redis_value.update(users_dict)
            redis_value.update(self.signal_data)
            redis_value['updated_at'] = updated_at
            self.redis_3.hset('remind_data_kline_futures', k, json.dumps(redis_value))

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
                #self.test_data_get()
                self._device_token_get()
                self.index()
                time.sleep(30)
            except Exception as e:
                logger.error('kline-futures指标监控 主函数异常{}'.format(e))
                time.sleep(60)

    def test_data_get(self):
        self.remind_data = {'okex-eos-this_week-15min-boll':[22]}
        self.ks = {'okex-eos-this_week-15min'}


if __name__ == '__main__':
    r = RemindKline()
    r.main()


