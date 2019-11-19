
from test2_scrapy.test.talib_test.IndexTool import IndexTool


it = IndexTool()
#it.kline_data_get()

def sarT(symbol='BTC_USDT'):
    # data = it.kline_data
    # sar = it.SAR()
    #x = data.close - sar
    #x = x[x > 0]
    #it.matplot((data.close, 'close'), (sar, 'SAR'), date_range=x.index)
    #result = zip(x.index, x, round(abs(x/data.close*100), 2))

    def signal(data):
        sar = it.SAR()
        up_down = data.close[-1] - sar[-1]
        percent = round(abs(up_down)/sar[-1]*100,2)
        gold_death = '金叉' if up_down > 0 else '死叉'

        signal = '{} |{} {}%|'.format(gold_death, round(abs(up_down), 4), percent)

        return signal

    it = IndexTool()
    day, h12, h6 = [signal(it.kline_data_get(market=None, type=type,
                                             symbol=symbol.lower())) for type in
                    ['1day', '12hour', '6hour']]
    print('交易对:{} 指标:SAR'.format(symbol))
    print('一天  12小时  6小时')
    print(day, h12, h6)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def sarT2():
    data_kline = it.kline_data
    data_sar = it.SAR()
    result = list(
        zip(data_kline.index, data_kline.low, data_sar, data_kline.close,
            data_kline.high, data_kline.close - data_sar))
    day_num = 0
    profit = 0
    x = 0
    for r in result:
        if r[-1] < 0:
            if day_num == 0:
                low = r[1]
                print(r[1])
            day_num += 1
            print(r, low - r[2])
            x = low - r[2]
        elif r[-1] > 0:
            if day_num:
                print(r, '------------------------天数：', day_num, '回落：',
                      r[-2] - r[-3])
                day_num = 0
                profit += x
                print(x)

    print(profit)

def sarT3():
    data = it.kline_data
    sar = it.SAR()
    x = data.close - sar
    result = list(zip(data.index, data.close, x))
    profit = []
    buy = None
    for index in range(1, len(result)):
        r = result[index]
        if result[index][-1] > 0 and result[index-1][-1] < 0:
            print(r, '买入:', r[1])
            buy = result[index][1]
        elif result[index][-1] < 0 and result[index-1][-1] > 0:
            print(r, '卖出:', r[1])
            sell = result[index][1]
            if buy:
                #profit.append(sell - buy)
                profit.append((sell/buy - 1)*100)
    profit = profit[2:]
    print(len(profit), profit)
    print(sum(profit))
    print(len([v for v in profit if v > 0]))

def macdT():
    data = it.kline_data
    DIF, DEA, MACD = it.MACD()
    result = list(zip(data.index, data.close, MACD))
    profit = []
    buy = None
    for index in range(1, len(result)):
        r = result[index]
        if result[index][-1] > 0 and result[index - 1][-1] < 0:
            print(r, '买入:', result[index-3])
            buy = result[index-3][1]
        elif result[index][-1] < 0 and result[index - 1][-1] > 0:
            print(r, '卖出:', result[index-3])
            sell = result[index-3][1]
            if buy:
                profit.append(sell - buy)
                #profit.append((sell / buy - 1) * 100)
    profit = profit[2:]
    print(len(profit), profit)
    print(sum(profit))
    print(len([v for v in profit if v > 0]))

def macdT2():
    """
    判断连涨趋势
    :return: 
    """
    data = it.kline_data
    DIF, DEA, MACD = it.MACD()
    date = data.index
    dates = []
    for index in range(3,len(data)):
        #print(index)
        # if MACD[index] > MACD[index-1] > MACD[index-2] > MACD[index-3]:
        #     print(date[index])
        #     dates.append(date[index])
        if MACD[index] < MACD[index-1] < MACD[index-2] < MACD[index-3]:
            print(date[index])
            dates.append(date[index])
    it.matplot((data.close, 'close'), date_range=dates)

def macdT3(symbol='BTC_USDT'):
    """
    判断当前趋势
    :return: 
    """

    def index_process(DIF, DEA, MACD, percent):
        short_long = '多头' if DIF[-1] > 0 and DEA[-1] > 0 else '空头'
        up = 0
        down = 0
        for i in range(2,len(MACD)+1):
            orgin_order = list(MACD[-i:])
            new_order = sorted(orgin_order)
            new_order_r = sorted(orgin_order, reverse=True)
            if orgin_order == new_order:
                up +=1
            elif orgin_order == new_order_r:
                down -=1
            else:
                break
        # ←↑→↓↖↙↗↘↕
        up_down = up if up > abs(down) else down
        up_down = '↑↗({})'.format(up_down) if up_down > 0 else \
                '↓↘({})'.format(abs(up_down))

        stable = 0
        for i in range(1, len(percent)):
            if abs(percent[-i]) < 1:
                stable += 1
            else:
                break
        stable = '连续平稳天数:{}'.format(stable) if stable > 0 else ''

        gold_death = '金叉' if MACD[-1] > 0 else '死叉'

        return '{} {}'.format(gold_death, up_down)

    result = []
    it = IndexTool()
    for type in ['1day', '12hour', '6hour']:
        data = it.kline_data_get(market=None, symbol=symbol.lower(), type=type)
        DIF, DEA, MACD = it.MACD()
        MACD *= 2
        percent = list(round(MACD / data.close * 100, 2))
        r = index_process(DIF, DEA, MACD, percent)
        result.append(r)

    day, h12, h6 = result
    print('交易对:{} 指标:MACD'.format(symbol))
    print('一天  12小时  6小时')
    print(day, h12, h6)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def macdT4():
    """
    趋势图
    :return: 
    """
    data = it.kline_data
    DIF, DEA, MACD = it.MACD()
    MACD *= 2
    it.matplot((DIF/data.close*100, 'DIF'), (DEA/data.close*100, 'DEA'))

def kdjT():
    data = it.kline_data
    K, D, J = it.KDJ()
    it.matplot((K, 'K'), (D, 'D'))

def kdjT2(symbol='BTC_USDT'):

    def signal(data):
        K, D = it.KDJ_2()
        up = 0
        down = 0
        for i in range(2, len(K) + 1):
            orgin_order = list(K[-i:])
            new_order = sorted(orgin_order)
            new_order_r = sorted(orgin_order, reverse=True)
            if orgin_order == new_order:
                up += 1
            elif orgin_order == new_order_r:
                down -= 1
            else:
                break
        #←↑→↓↖↙↗↘↕
        gold_death = '金叉' if K[-1] > D[-1] else '死叉'
        up_down = '↑↗' if up else '↓↘'

        signal = '{} {}({})'.format(gold_death,up_down,abs(up+down))

        return signal

    it = IndexTool()
    day, h12, h6 = [signal(it.kline_data_get(market=None, type=type,
                    symbol=symbol.lower())) for type in ['1day', '12hour', '6hour']]
    print('交易对:{} 指标:KDJ'.format(symbol))
    print('一天  12小时  6小时')
    print(day, h12, h6)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def emaT():
    data = it.kline_data
    ema = it.EMA()
    x = ((data.low+data.high)/2) - ema
    x = x[x > 0]
    #print(x.index)
    it.matplot((data.close, 'close'), (ema, 'EMA'), date_range=x.index)

def emaT2():
    data = it.kline_data

    ema7, ema30 = it.EMA(period=[7,30])
    x = ema7 - ema7.shift(1)
    x = x[x > 0]
    it.matplot((ema7, 'EMA7'), (ema30, 'EMA30'), date_range=x.index)

def emaT3(symbol='BTC_USDT'):

    def signal(data):
        ema7, ema30 = it.EMA(period=[7, 30])

        up = 0
        down = 0
        for i in range(2, len(ema7) + 1):
            orgin_order = list(ema7[-i:])
            new_order = sorted(orgin_order)
            new_order_r = sorted(orgin_order, reverse=True)
            if orgin_order == new_order:
                up += 1
            elif orgin_order == new_order_r:
                down -= 1
            else:
                break
        gold_death = '金叉' if ema7[-1] > ema30[-1] else '死叉'
        up_down = '↑↗' if up else '↓↘'
        signal = '{} {}({})'.format(gold_death, up_down, abs(up + down))

        return signal

    it = IndexTool()
    day, h12, h6 = [signal(it.kline_data_get(market=None, type=type,
                                             symbol=symbol.lower())) for type in
                    ['1day', '12hour', '6hour']]
    print('交易对:{} 指标:EMA'.format(symbol))
    print('一天  12小时  6小时')
    print(day, h12, h6)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def bollT(symbol='BTC_USDT'):

    def signal(data):
        VB, BOLL, LB = it.BOLL()
        price = data.close[-1]

        signal = None
        if price < LB[-1]:
            signal = '超低'
        elif LB[-1] <= price < BOLL[-1]:
            signal = '中下'
        elif BOLL[-1] <= price < VB[-1]:
            signal = '中上'
        elif VB[-1] <= price:
            signal = '超高'

        return signal

    it = IndexTool()
    day, h12, h6 = [signal(it.kline_data_get(market=None, type=type,
                                             symbol=symbol.lower())) for type in
                    ['1day', '12hour', '6hour']]
    print('交易对:{} 指标:BOLL'.format(symbol))
    print('一天  12小时  6小时')
    print(day, h12, h6)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

symbol = 'ETH_USDT'
#sarT2()
sarT(symbol)
#sarT3()

#macdT()
#macdT2()
macdT3(symbol)
#macdT4()

#kdjT()
kdjT2(symbol)

#
#emaT2()
emaT3(symbol)

bollT(symbol)