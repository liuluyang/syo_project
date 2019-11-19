from binance.client import Client
"""
API Key:
VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw
Secret Key:  For your security, your API Secret Key will only be displayed at the time it is created. If you lose this key, you will need to delete your API and set up a new one.
CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj
"""
api_key = 'VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw'
api_secret = 'CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj'

client = Client(api_key, api_secret)
print (client)


# # get market depth
# depth = client.get_order_book(symbol='BNBBTC')
# print (depth)

# place a test market buy order, to place an actual order use the create_order function
# order = client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=1,
#     recvWindow=5000
#     )

# get all symbol prices
# prices = client.get_all_tickers()
# print (prices)

# withdraw 100 ETH
# check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException, BinanceWithdrawException
# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")

# fetch list of withdrawals
# withdraws = client.get_withdraw_history()
#
# # fetch list of ETH withdrawals
# eth_withdraws = client.get_withdraw_history(asset='ETH')
#
# # get a deposit address for BTC
# address = client.get_deposit_address(asset='BTC')

# start aggregated trade websocket for BNBBTC
# def process_message(msg):
#     print (1)
#     print("message type: {}".format(msg['e']))
#     print(msg)
#     # do something

# from binance.websockets import BinanceSocketManager
# bm = BinanceSocketManager(client)
# # #bm.start_aggtrade_socket('BNBBTC', process_message)
# # conn_key = bm.start_trade_socket('BNBBTC', process_message)
# # bm.start()
# conn_key = bm.start_aggtrade_socket('ETHBTC', process_message)
# print (conn_key)
# bm.start()

# def process_m_message(msg):
#     print("stream: {} data: {}".format(msg['stream'], msg['data']))
#
# # pass a list of stream names
# conn_key = bm.start_multiplex_socket(['bnbbtc@aggTrade', 'neobtc@ticker'],
#                                      process_m_message)
# bm.start()


# get historical kline data from any date range

# fetch 1 minute klines for the last day up until now
#klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# fetch 30 minute klines for the last month of 2017
#klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
#klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")