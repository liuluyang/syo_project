
import requests



tickers = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries').json()
print(tickers)

symbols = requests.get('https://bittrex.com/api/v1.1/public/getmarkets').json()
print(symbols)