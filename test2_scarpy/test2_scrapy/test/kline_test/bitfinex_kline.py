
from websocket import create_connection
import json, time
"""
{"event":"info","version":1.1,"serverId":"3abf9aaf-b61b-4174-8221-91984fe326a4","platform":{"status":1}}
{"event":"subscribed","channel":"candles","chanId":189678,"key":"trade:30m:tBTCUSD"}



[189678,[1541489400000,6462.44372228,6462.6,6465.3,6462.4,61.17710957]]
[189678,[1541491200000,6462.6,6462.6,6462.6,6462.5,5.50789395]]
[189678,"hb"]



{
   "event":"unsubscribe",
   "chanId":"<CHANNEL_ID>" #189678
}
"""

data_send = {
  "event": "subscribe",
  "channel": "candles",
  "key": "trade:1m:tBTCUSD"
}
data_send = json.dumps(data_send)

ws = create_connection('wss://api.bitfinex.com/ws')
ws.send(data_send)

while True:
    data_recv = ws.recv()
    print(data_recv)