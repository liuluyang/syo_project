import requests
import time

"""
交易精英趋向指标
"""
interval_5m = 0
interval_15m = 1
interval_1h = 2


def elite_get():
    allSymbol = requests.post('https://www.okex.me/v2/futures/pc/market/allSymbol.do').json()

    if allSymbol.get('msg') == 'success':
        for info in allSymbol['data']:
            print(info)
            interval = interval_5m
            scale_url = 'https://www.okex.me/v2/futures/pc/public/eliteScale.do?' \
                           'symbol={}&type={}'.format(info['symbol'], interval)
            scaleInfo = requests.get(scale_url).json()
            if scaleInfo.get('msg') == 'success':
                data = scaleInfo['data']
                #print(len(data), data)
                #时间戳 做多 做空
                print(list(
                    zip(data['timedata'], data['buydata'], data['selldata'])))

            ratio_url = 'https://www.okex.me/v2/futures/pc/public/getFuturePositionRatio.do?' \
                        'symbol={}&type={}'.format(info['symbol'], interval)
            ratioInfo = requests.get(ratio_url).json()
            if ratioInfo.get('msg') == 'success':
                data = ratioInfo['data']
                #print(len(data), data)
                #时间戳 多头 空头
                print(list(
                    zip(data['timedata'], data['buydata'], data['selldata'])))

            print('____________________')
            time.sleep(0.1)

elite_get()