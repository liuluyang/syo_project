from websocket import create_connection
import json

ws = create_connection('wss://ws.exx.com/websocket')

data_send = {
    "dataType":"1_KLINE_30M_BTC_USDT",
    "dataSize":1,
    "action":"ADD"
}

data_send = json.dumps(data_send)
ws.send(data_send)
print (ws.recv())

