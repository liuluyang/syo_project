import requests


tickers = requests.get('http://api.zb.cn/data/v1/allTicker').json()

print(len(tickers))
for t in tickers:
    print(t)