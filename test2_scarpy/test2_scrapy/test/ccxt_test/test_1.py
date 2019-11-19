
from websocket import create_connection
import json, time

data_send = {
  "event": "subscribe",
  "channel": "trades",
  "pair": "BTCUSD"
}
data_send = json.dumps(data_send)

ws = create_connection('wss://api.bitfinex.com/ws')
ws.send(data_send)

while True:
    data_recv = ws.recv()
    print(data_recv)

