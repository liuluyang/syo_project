import requests


r = requests.get('https://api.bithumb.com/public/transaction_history/BTC').json()

data = r['data']

for d in data:
    print(d)