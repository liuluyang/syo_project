import requests
import time


"""
持仓总量
"""

interval_1h = 1
interval_4h = 2
interval_12h = 3

symbolInfo = requests.post('https://www.okex.me/v2/futures/pc/queryInfo/symbolInfo.do').json()
if symbolInfo.get('msg') == 'success':
    pass
    # for info in symbolInfo['data']:
    #     print(info)

def position_get():
    allSymbol = requests.post('https://www.okex.me/v2/futures/pc/market/allSymbol.do').json()

    if allSymbol.get('msg') == 'success':
        for info in allSymbol['data']:
            print(info)
            position_url = 'https://www.okex.me/v2/futures/pc/public/futureVolume.do?' \
                           'symbol={}&type={}'.format(info['symbol'], interval_1h)
            #print(position_url)
            positionInfo = requests.get(position_url).json()
            if positionInfo.get('msg') == 'success':
                data = positionInfo['data']
                print(len(data), data)
            #print(positionInfo)
            print('____________________')
            time.sleep(0.1)

position_get()
