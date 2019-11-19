import requests


url_currency = 'https://test1.bicoin.info/stock/getOutOfStockList?' \
              'pageNum=1&pageSize=100&host=leekassit&symbolStr={}'

ordersInfo = requests.get(url_currency.format('btc'))

status_code = ordersInfo.status_code
text = ordersInfo.text
print(ordersInfo)
print(status_code, type(text))