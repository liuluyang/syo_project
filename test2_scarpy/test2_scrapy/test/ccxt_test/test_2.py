from ccxt.bitfinex import bitfinex
from ccxt.bittrex import bittrex


b = bitfinex()
print(len(b.fetch_markets()))

# bt = bittrex()
# print(bt.fetch_markets())
# tickers = bt.fetch_tickers()
#
# for k,v in tickers.items():
#     print(k, v)