
from test2_scrapy.test.talib_test.IndexTool import IndexTool


class IndexTrend(object):

    def __init__(self, symbol='BTC_USDT'):
        self.it = IndexTool()
        self.data = None
        self.symbol = symbol
        self.price = None

    def KDJ(self):
        name = 'KDJ'
        K, D = self.it.KDJ_2()
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

        signal = '{} {}({})'.format(gold_death, up_down, abs(up+down))

        return name, signal

    def MACD(self):
        name = 'MACD'
        DIF, DEA, MACD = self.it.MACD()
        MACD *= 2
        up = 0
        down = 0
        for i in range(2, len(MACD) + 1):
            orgin_order = list(MACD[-i:])
            new_order = sorted(orgin_order)
            new_order_r = sorted(orgin_order, reverse=True)
            if orgin_order == new_order:
                up += 1
            elif orgin_order == new_order_r:
                down -= 1
            else:
                break
        # ←↑→↓↖↙↗↘↕
        up_down = up if up > abs(down) else down
        up_down = '↑↗({})'.format(up_down) if up_down > 0 else \
            '↓↘({})'.format(abs(up_down))

        gold_death = '金叉' if MACD[-1] > 0 else '死叉'

        signal = '{} {}'.format(gold_death, up_down)

        return name, signal

    def EMA(self):
        name = 'EMA'
        ema7, ema30 = self.it.EMA(period=[7, 30])
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

        return name, signal

    def SAR(self):
        name = 'SAR'
        sar = self.it.SAR()
        up_down = self.data.close[-1] - sar[-1]
        percent = round(abs(up_down) / sar[-1] * 100, 2)
        gold_death = '金叉' if up_down > 0 else '死叉'

        signal = '{} |{} {}%|'.format(gold_death, round(abs(up_down), 4), percent)

        return name, signal

    def BOLL(self):
        name = 'BOLL'
        VB, BOLL, LB = self.it.BOLL()
        price = self.data.close[-1]
        signal = None
        if price < LB[-1]:
            signal = '超低'
        elif LB[-1] <= price < BOLL[-1]:
            signal = '中下'
        elif BOLL[-1] <= price < VB[-1]:
            signal = '中上'
        elif VB[-1] <= price:
            signal = '超高'

        return name, signal

    def signal_desc(self, result):
        index = result['index']

        for k in index:
            v = result[k]
            value = ''.join(v)
            if k in ['MACD', 'KDJ', 'EMA']:
                desc = '-'
                if value.count('↑↗') == 3:
                    desc = '看涨'
                elif value.count('↓↘') == 3:
                    desc = '看跌'
                result[k + '_DESC'] = desc
                result[k].append(desc)
            elif k in ['SAR']:
                desc = '-'
                if value.count('金叉') == 3:
                    desc = '看涨'
                elif value.count('死叉') == 3:
                    desc = '看跌'
                result[k + '_DESC'] = desc
                result[k].append(desc)
            else:
                desc = '-'
                result[k + '_DESC'] = desc
                result[k].append(desc)

        return result

    def main(self):

        index_list = [self.KDJ, self.MACD, self.EMA, self.SAR, self.BOLL]
        period_list = ['1day', '12hour', '6hour']
        symbol = self.symbol
        result = {'period':period_list, 'symbol':self.symbol}
        index = set()
        for period in period_list:
            self.it.kline_data_get(market=None, type=period, symbol=symbol.lower())
            self.data = self.it.kline_data
            for cal in index_list:
                name, signal = cal()
                index.add(name)
                print(signal)
                if name in result:
                    result[name].append(signal)
                else:
                    result[name] = [signal]
        result['price'] = self.data.close[-1]
        result['index'] = index
        result = self.signal_desc(result)
        print(result)


IT = IndexTrend()
IT.main()

