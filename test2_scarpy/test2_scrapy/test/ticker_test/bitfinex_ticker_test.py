from websocket import create_connection
import json, time

"""
{"event":"info","version":1.1,"serverId":"74b49ff3-6628-42f6-9833-7a65a0933241","platform":{"status":1}}
{"event":"subscribed","channel":"ticker","chanId":4169,"pair":"BTCUSD"}
[4169,6467,58.1968253,6467.1,44.68962228,-4.49618833,-0.0007,6467.1,4525.74311089,6493.08496207,6435.3]
[4169,"hb"]
[4169,6467.3,63.66678672,6467.6,39.95363958,-4.59618833,-0.0007,6467,4525.75311089,6493.08496207,6435.3]
                                            change_price  change,  last  volume    high     lower
[4169,"hb"]

"""

data_send = {
  "event": "subscribe",
  "channel": "ticker",
  "symbol": "tBTCUSD"
}
data_send = json.dumps(data_send)

ws = create_connection('wss://api.bitfinex.com/ws')
ws.send(data_send)

while True:
    data_recv = ws.recv()
    print(data_recv)
