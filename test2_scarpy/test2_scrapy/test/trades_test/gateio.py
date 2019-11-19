from websocket import create_connection
import time
import requests
import json

time_now = int(time.time())
"""
{
    "error": null,
    "result": [
        {
            "id": 91538039,
            "time": 1537322562.196229,
            "price": "6345",
            "amount": "0.00423089",
            "type": "sell"
        },
        {
            "id": 91537975,
            "time": 1537322529.4088731,
            "price": "6345",
            "amount": "0.0163",
            "type": "sell"
        }
    ],
    "id": 12309
}
"""
def gateio_trades_get():
    ws = create_connection("wss://ws.gateio.io/v3/")

    ws.send('{"id":12309, "method":"trades.query", "params":["BTC_USDT", 50,  91582989]}')
    #所有交易对共用自增连续id
    #新-旧 返回的数据不包含last_id这条
    #交易时间m
    data = ws.recv()
    data = json.loads(data)
    print (len(data['result']))
    return data

print (gateio_trades_get())


from binance.client import Client


"""
[
{'id': 1, 'price': '12.49000000', 'qty': '8.09000000', 'time': 1527483605628, 
'isBuyerMaker': True, 'isBestMatch': True}, 
{'id': 2, 'price': '12.49000000', 'qty': '5.84000000', 'time': 1527483605713, 
'isBuyerMaker': True, 'isBestMatch': True}
]
"""
#binance
def binance_trade_get():
    api_key = 'VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw'
    api_secret = 'CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj'

    client = Client(api_key, api_secret)

    params = {'symbol':'EOSUSDT', 'limit':2, 'fromId':2}
    params = {'symbol': 'EOSUSDT', 'limit': 500, 'fromId':7889976}
    data = client.get_historical_trades(**params)
    #每个交易对拥有自增连续id
    #旧-新 返回的数据包含fromId这条
    #交易时间ms
    print (len(data))
    return data

#print (binance_trade_get())

def okex_trades_get(symbol, since=0):
    """
    symbol:ltc_usdt
    since:
    :return: max 60条
    """
    url = 'https://www.okex.com/api/v1/trades.do?symbol={symbol}&since={since}'
    url = url.format(symbol=symbol, since=since)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    print (len(data))
    return data
#每个交易对拥有自增连续id
#旧-新 返回的数据不包含since这条
#交易时间ms
#print (okex_trades_get('eos_usdt'))

def huobi_trades_get(symbol, size=100):
    """
    symbol:btcusdt
    size:default and max 2000
    :return: 
    """
    url = 'https://api.huobi.pro/market/history/trade?symbol={symbol}&size={size}'
    url = url.format(symbol=symbol, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data
#所有交易对共用自增连续id
#新-旧 返回的数据不包含last_id这条
#交易时间ms
# data = huobi_trades_get('btcusdt')
# for d in data['data']:
#     print (d)
