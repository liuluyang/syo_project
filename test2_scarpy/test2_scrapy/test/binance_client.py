from binance.client import Client
import json
import time

#BTC BNB ETH USDT
api_key = 'VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw'
api_secret = 'CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj'

client = Client(api_key, api_secret)

print (client.ping())

for i in range(100):
  c = Client(api_key, api_secret)
  print (c.ping(), i)

# depth = client.get_order_book(symbol='BNBBTC')
# print (depth)
#
#prices = client.get_all_tickers()
# print (prices)
# print (len(prices), prices)
#
# while True:
#     prices = client.get_all_tickers()
#     print (prices)
#     time.sleep(2)
while True:
    t = int(time.time())
    period = 60
    num  = 5
    d = {1,60,300,600,1800,3600,3600*24,3600*24*7}
    change_period_dict = {60:'1m',300:'5m',1800:'30m',3600:'1h',3600*24:'1d',3600*24*7:'1w'}
    period_binance = change_period_dict.get(period)
    klines = client.get_historical_klines('BTCUSDT', period_binance,
                                          (t-num*period)*1000, t*1000)
    print (klines)

# tickers = client.get_ticker()
# print (tickers)
# for ticket in tickers:
#     print (ticket)
#     for k,v in ticket.items():
#         print (k,v)

# while True:
#     print (time.time())
#     tickers = client.get_ticker()
#     print(time.time())
#     print(tickers)
#     time.sleep(1)




"""
symbol POLYBNB
priceChange -0.00141000
priceChangePercent -7.234
weightedAvgPrice 0.01883632
prevClosePrice 0.01978000
lastPrice 0.01808000
lastQty 114.70000000
bidPrice 0.01809000
bidQty 113.20000000
askPrice 0.01878000
askQty 1311.50000000
openPrice 0.01949000
highPrice 0.02006000
lowPrice 0.01808000
volume 34347.20000000
quoteVolume 646.97489600
openTime 1533873663874
closeTime 1533960063874
firstId 5915
lastId 6098
count 184
"""

d = {
  "e": "24hrTicker",  #// Event type                       period
  "E": 123456789,     #// Event time
  "s": "BNBBTC",      #/ Symbol
  "p": "0.0015",      #// Price change
  "P": "250.00",      #// Price change percent              change
  "w": "0.0018",      #// Weighted average price
  "x": "0.0009",      #// Previous day's close price
  "c": "0.0025",      #// Current day's close price         close
  "Q": "10",          #// Close trade's quantity
  "b": "0.0024",      #// Best bid price
  "B": "10",          #// Best bid quantity
  "a": "0.0026",      #// Best ask price
  "A": "100",         #// Best ask quantity
  "o": "0.0010",      #// Open price                        open
  "h": "0.0025",      #// High price                        high
  "l": "0.0010",      #// Low price                         low
  "v": "10000",       #// Total traded base asset volume      baseVolume
  "q": "18",          #// Total traded quote asset volume     quoteVolume
  "O": 0,             #// Statistics open time
  "C": 86400000,      #// Statistics close time
  "F": 0,             #// First trade ID
  "L": 18150,         #// Last trade Id
  "n": 18151          #// Total number of trades
}