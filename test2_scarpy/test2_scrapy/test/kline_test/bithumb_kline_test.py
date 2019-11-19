
import requests

url = 'https://cn.bithumb.com/resources/chart/ABT_xcoinTrade_01M.json?' \
      'symbol=ABT&resolution=0.5&from=1539765680&to=1542357740&strTime=1542357680159'

url_01 = 'https://cn.bithumb.com/resources/chart/ABT_xcoinTrade_01M.json?' \
         'symbol=ABT&resolution=100&from=1537470800&to=1542358048&strTime=1542357988835'
url_24h = 'https://cn.bithumb.com/resources/chart/ABT_xcoinTrade_24H.json?' \
          'symbol=ABT&resolution=0.5&from=1536296400&to=1542358060&strTime=1542358000311'

data_kline = requests.get(url_24h).json()
for d in data_kline:
    print(d)

print(len(data_kline))
