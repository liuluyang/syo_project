from websocket import create_connection as create
import json

"""
b'{"requestId":"1","candlesSnapshot":
{"candles":[
{"market":"BTC-USDT","time":"2018-10-29T03:16:00Z","open":"6497.42","high":"6497.42","low":"6497.19","close":"6497.19"},{"market":"BTC-USDT","time":"2018-10-29T03:15:00Z","open":"6497.78","high":"6498.95","low":"6497.46","close":"6497.46"},{"market":"BTC-USDT","time":"2018-10-29T03:14:00Z","open":"6498.17","high":"6498.17","low":"6484.0","close":"6497.78"},{"market":"BTC-USDT","time":"2018-10-29T03:13:00Z","open":"6498.55","high":"6498.56","low":"6498.2","close":"6498.2"},{"market":"BTC-USDT","time":"2018-10-29T03:12:00Z","open":"6506.45","high":"6506.45","low":"6498.57","close":"6498.57"},{"market":"BTC-USDT","time":"2018-10-29T03:11:00Z","open":"6494.66","high":"6506.47","low":"6494.66","close":"6506.47"},{"market":"BTC-USDT","time":"2018-10-29T03:10:00Z","open":"6498.6","high":"6506.18","low":"6494.65","close":"6494.66"},{"market":"BTC-USDT","time":"2018-10-29T03:09:00Z","open":"6498.59","high":"6506.18","low":"6498.58","close":"6498.9"},{"market":"BTC-USDT","time":"2018-10-29T03:08:00Z","open":"6498.89","high":"6506.18","low":"6498.58","close":"6506.18"},{"market":"BTC-USDT","time":"2018-10-29T03:07:00Z","open":"6499.03","high":"6506.06","low":"6498.59","close":"6506.03"},{"market":"BTC-USDT","time":"2018-10-29T03:06:00Z","open":"6498.82","high":"6506.42","low":"6484.02","close":"6506.28"},{"market":"BTC-USDT","time":"2018-10-29T03:05:00Z","open":"6498.03","high":"6499.24","low":"6498.03","close":"6499.12"},{"market":"BTC-USDT","time":"2018-10-29T03:04:00Z","open":"6498.37","high":"6505.79","low":"6498.05","close":"6498.33"},{"market":"BTC-USDT","time":"2018-10-29T03:03:00Z","open":"6499.06","high":"6506.16","low":"6498.4","close":"6498.7"},{"market":"BTC-USDT","time":"2018-10-29T03:02:00Z","open":"6499.21","high":"6499.21","low":"6498.77","close":"6498.77"},{"market":"BTC-USDT","time":"2018-10-29T03:01:00Z","open":"6512.95","high":"6512.95","low":"6512.95","close":"6512.95"},{"market":"BTC-USDT","time":"2018-10-29T03:00:00Z","open":"6512.95","high":"6512.95","low":"6512.95","close":"6512.95"},{"market":"BTC-USDT","time":"2018-10-29T02:59:00Z","open":"6484.02","high":"6484.02","low":"6484.02","close":"6484.02"},{"market":"BTC-USDT","time":"2018-10-29T02:58:00Z","open":"6484.02","high":"6484.02","low":"6484.02","close":"6484.02"},{"market":"BTC-USDT","time":"2018-10-29T02:57:00Z","open":"6484.02","high":"6484.02","low":"6484.02","close":"6484.02"}]}}'


b'{"requestId":"1","candleUpdate":{"candle":{"market":"BTC-USDT","time":"2018-10-29T03:16:00Z","open":"6497.42","high":"6497.42","low":"6497.17","close":"6497.17"}}}'
"""


ws = create('wss://big.one/ws/v2', header={'sec-websocket-protocol':'json'},
            subprotocols=['json'])

data_send = {"requestId": "1", "subscribeMarketCandlesRequest":
    {"market":"BTC-USDT", "period": "MIN1"}}
data_send = json.dumps(data_send)

ws.send(data_send)

while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv.decode())
    print(data_recv)

    candles = data_recv.get('candlesSnapshot', {}).get('candles')
    if candles:
        print(len(candles))
