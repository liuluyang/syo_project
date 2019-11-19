from websocket import create_connection
ws = create_connection("wss://ws.gateio.io/v3/")
ws.send('{"id":12312, "method":"trades.subscribe", "params":["ETH_USDT", "BTC_USDT"]}')

while True:
    print(ws.recv())