import requests
import time
import threading
# print (time.time())
# data = requests.get('https://www.okex.com/api/v1/kline.do?symbol=ltc_btc&type=1min&size=100',
#                  headers={'content-type':'application/x-www-form-urlencoded'}
#                  ).json()
#
# print (time.time())
# for num,per in enumerate(data):
#     print (num, per)
# print (time.time())

def data_kline_get(symbol, type, size=100):
    """
    symbol:ltc_usdt
    type:1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    size:default and max 2000
    :return: 
    """
    url = 'https://www.okex.com/api/v1/kline.do?symbol={symbol}&type={type}&size={size}'
    url = url.format(symbol=symbol, type=type, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data

#print (data_kline_get('ltc_btc', '1min'))
for i in data_kline_get('ltc_btc', '1min'):
    print (i)


if __name__=='__main__':
    pass
    # for i in range(2,4):
    #     t = threading.Thread(target=data_kline_get, args=('ltc_btc', '1min', i))
    #     t.start()