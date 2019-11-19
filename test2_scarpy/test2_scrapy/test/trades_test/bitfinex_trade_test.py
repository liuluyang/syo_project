from ccxt.bitfinex import bitfinex


b = bitfinex()
print(b.fetch_markets())