
from websocket import create_connection
import json, time

"""
[557666,"te","7422102-BTCUSD",1541491466,6462.5,-0.607]
[557666,"tu","7422102-BTCUSD",309120343,1541491466,6462.5,-0.607]
[557666,"hb"]


{
  "event": "subscribe",
  "channel": "trades",
  "symbol": "tBTCUSD"
}

"""

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

