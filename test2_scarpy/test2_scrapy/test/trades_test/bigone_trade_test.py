from websocket import create_connection as create
import json

"""
{"requestId":"1","tradeUpdate":
{"trade":
{"id":"36496929","price":"6499.59","amount":"0.03","market":"BTC-USDT",
"createdAt":"2018-10-29T06:04:37.529022212Z","makerOrder":
{"id":"186414836","price":"6499.59","stopPrice":"0","amount":"0.03",
"market":"BTC-USDT","state":"FILLED","filledAmount":"0.03","filledFees":
"0.00003","avgDealPrice":"6499.59","createdAt":"2018-10-29T06:04:37Z",
"updatedAt":"2018-10-29T06:04:37.540302494Z"},"takerOrder":
{"id":"186414837","price":"6499.29","stopPrice":"0","amount":"0.03",
"market":"BTC-USDT","side":"ASK","state":"FILLED","filledAmount":"0.03",
"filledFees":"0.1949877","avgDealPrice":"6499.59","createdAt":
"2018-10-29T06:04:37Z","updatedAt":"2018-10-29T06:04:37.542160577Z"}}}}


"""


ws = create('wss://big.one/ws/v2', header={'sec-websocket-protocol':'json'},
            subprotocols=['json'])

data_send = {"requestId": "1", "subscribeMarketTradesRequest":{"market":"BTC-USDT"}}
data_send = json.dumps(data_send)

ws.send(data_send)

while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv.decode())
    tradeUpdate = data_recv.get('tradeUpdate')
    if tradeUpdate:
        d = tradeUpdate['trade']
        d['type'] = 'buy' if d['makerOrder'].get('side') else 'sell'
        if d['type']=='buy':
            print('买入 绿色',d['createdAt'])
        else:
            print('卖出 红色', d['createdAt'])
