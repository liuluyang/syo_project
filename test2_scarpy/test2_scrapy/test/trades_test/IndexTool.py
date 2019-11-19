import requests
import json
import time
from websocket import create_connection
import pandas as pd
import talib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


class IndexTool(object):
    def __init__(self):
        self.kline_data = None

    def kline_okex(self, symbol='btc_usdt', nums=2000, type='1day'):
        """ 
        
        :param symbol: 
        :param nums: 
        :param type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour
                    /4hour/6hour/12hour
        :return: 
        """
        url = 'https://www.okex.com/api/v1/kline.do?symbol={symbol}&type={type}&size={size}'
        url = url.format(symbol=symbol, type=type, size=nums)
        data = requests.get(url, headers={
            'content-type': 'application/x-www-form-urlencoded'}).json()
        new_result = []
        for r in data:
            new_result.append([r[0], r[4], r[2], r[3], r[1], r[5]])

        return new_result

    def kline_base(self, symbol='btc_usdt', nums=2000, market='okex'):
        """
        
        :param symbol: 
        :param nums: 
        :param type: 
        :param market: 
        :return: 
        """
        data_send = {'market': market, 'method': 'kline',
                     'symbol': symbol.upper(),
                     'params': {'num': nums, 'period': 3600 * 24}, 'id': 1}
        data_send = json.dumps(data_send)
        ws = create_connection('ws://47.52.115.31/v1/market/')
        ws.send(data_send)

        data_recv = ws.recv()
        data = json.loads(data_recv)['data']

        return data

    def kline_data_get(self, symbol='btc_usdt', nums=2000, type='1day',
                       market='okex'):
        """
        
        :param symbol: 
        :param nums: 
        :param type: 
        :param market: 
        :return: 
        """
        if market:
            data = self.kline_base(symbol, nums, market)
        else:
            data = self.kline_okex(symbol, nums, type)

        for d in data:
            for i in range(1, 6):
                d[i] = float(d[i])
            d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0] / 1000))

        dataFrame = pd.DataFrame(data, columns=['date', 'close', 'high', 'low',
                                                'open', 'volume'])
        dataFrame.index = dataFrame.date
        dataFrame.index = pd.to_datetime(dataFrame.index, format='%Y-%m-%d %H:%M:%S')
        dataFrame = dataFrame.iloc[:, 1:]
        self.kline_data = dataFrame

        return dataFrame

    def MA(self, data=None, period=7, matype=0):
        """
        0->SMA  1->EMA  2->WMA
        :param data: 
        :param period: 
        :param matype: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data
        if isinstance(period, int):
            period = [period]
        if isinstance(period, list):
            result = []
            for p in period:
                r= talib.MA(data.close, timeperiod=p, matype=matype)
                result.append(r)

            return tuple(result) if len(result) > 1 else result[0]

    def SMA(self, data=None, period=7):
        """
        简单移动平均
        :param data: 
        :param period: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data
        if isinstance(period, int):
            period = [period]
        if isinstance(period, list):
            result = []
            for p in period:
                r= talib.SMA(data.close, timeperiod=p)
                result.append(r)

            return tuple(result) if len(result) > 1 else result[0]

    def WMA(self, data=None, period=7):
        """
        加权移动平均
        :param data: 
        :param period: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data
        if isinstance(period, int):
            period = [period]
        if isinstance(period, list):
            result = []
            for p in period:
                r= talib.WMA(data.close, timeperiod=p)
                result.append(r)

            return tuple(result) if len(result) > 1 else result[0]

    def EMA(self, data=None, period=7):
        """
        指数移动平均
        :param data: 
        :param period: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data
        if isinstance(period, int):
            period = [period]
        if isinstance(period, list):
            result = []
            for p in period:
                r= talib.EMA(data.close, timeperiod=p)
                result.append(r)

            return tuple(result) if len(result) > 1 else result[0]

    def MACD(self, data=None):
        """
        指数平滑移动平均线
        :param data: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data

        DIF, DEA, MACD = talib.MACD(data.close, fastperiod=12, slowperiod=26,
                                    signalperiod=9)

        return DIF, DEA, MACD

    def SAR(self, data=None):
        """
        停损点转向指标(SAR抛物线指标)
        :param data: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data

        SAR = talib.SAR(data.high, data.low, acceleration=0.027, maximum=0.19)

        return SAR

    def KDJ(self, data=None):
        """
        随机指标
        :param data: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data

        KDJ = talib.STOCH(data.high, data.low, data.close, fastk_period=9,
                               slowk_period=3, slowk_matype=0,
                               slowd_period=3, slowd_matype=0)
        K, D = KDJ[0]-1, KDJ[1]
        J = K * 3 - D * 2

        return K, D, J

    def KDJ_2(self, data=None):
        """
        随机指标2
        :param data: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data

        period = 9
        K, D, J = 50, 50, 50
        high_list = data.high
        low_list = data.low
        close_list = data.close
        k = pd.Series(0.0, index=data.index)
        d = pd.Series(0.0, index=data.index)
        for i in range(period - 1, len(data)):
            high = max(high_list[i - period + 1:i + 1])
            low = min(low_list[i - period + 1:i + 1])
            close = close_list[i]
            x = 1 if high - low == 0 else high - low
            RSV = (close - low) / x * 100
            K = 2 / 3 * K + 1 / 3 * RSV
            D = 2 / 3 * D + 1 / 3 * K
            k[i] = round(K, 2)
            d[i] = round(D, 2)

        return k, d

    def BOLL(self, data=None):
        """
        布林线
        :param data: 
        :return: 
        """
        if not isinstance(data, pd.DataFrame):
            if not isinstance(self.kline_data, pd.DataFrame):
                self.kline_data_get()
            data = self.kline_data

        VB, BOLL, LB = talib.BBANDS(data.close, timeperiod=20, nbdevup=2,
                                    nbdevdn=2, matype=0)

        return VB, BOLL, LB

    def matplot(self, *args, **kwargs):
        if args:
            for data in args:
                plt.plot(data[0], label=data[1])
            plt.gca().xaxis.set_major_formatter(
                mdates.DateFormatter('%Y-%m-%d'))  # 設置x軸主刻度顯示格式（日期）
            # plt.gca().xaxis.set_major_locator(
            #     mdates.MonthLocator(interval=2))  # 設置x軸主刻度間距
            #date_range = pd.date_range(args[0][0].index[0],args[0][0].index[-1])
            #date_range = list(args[0][0].index[0:100])+list(args[0][0].index[200:300])
            date_range = kwargs.get('date_range', [])
            #print(date_range)
            plt.xticks(date_range)
            plt.legend(loc='best')
            plt.grid(True)
            plt.xlabel('日期')
            plt.rcParams['font.sans-serif'] = ['SimHei']
            #plt.title('BTC_USDT 日线收盘价')
            plt.show()


if __name__ == '__main__':
    it = IndexTool()
    it.kline_data_get()
    sma = it.SMA()
    wma = it.WMA()
    ema = it.EMA()
    macd = it.MACD()
    sar = it.SAR()
    kdj = it.KDJ()
    boll = it.BOLL()
    kdj_2 = it.KDJ_2()
    #print(sma)
    # print(wma)
    # print(ema)
    # print(macd[0])
    # print(sar)
    # print(kdj)
    # print(boll)
    #it.matplot((sma, 'SMA'))
    #print(kdj_2)