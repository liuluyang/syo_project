from websocket import create_connection
import requests
import json
import time

symbols = requests.get('https://data.gateio.io/api2/1/pairs').json()
ws = create_connection("wss://ws.gateio.io/v3/")

start = time.time()
for sym in symbols:
    print(sym)
    data_send_f = {"id":12312, "method":"ticker.subscribe", "params":["ETH_USDT"]}
    data_send_f['params'] = [sym]
    data_send = json.dumps(data_send_f)
    ws.send(data_send)
    print(ws.recv())
    print(ws.recv())
    time.sleep(0.1)

print(start, time.time())



# ws.send('{"id":12312, "method":"ticker.subscribe", "params":["ETH_USDT"]}')
# print (ws.recv())
# print (ws.recv())
# ws.send('{"id":12312, "method":"ticker.subscribe", "params":["BTC_USDT"]}')
# print (ws.recv())
# print (ws.recv())
# ws.send('{"id":12312, "method":"ticker.subscribe", "params":["EOS_USDT"]}')
# print (ws.recv())
# print (ws.recv())
# ws.send('{"id":12312, "method":"ticker.subscribe", "params":["LYM_USDT"]}')
# print (ws.recv())
# print (ws.recv())