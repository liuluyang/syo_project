from websocket import create_connection
import hmac
import base64
import hashlib
import time
import json

#secret_key = 'your secret key'

def get_sign(secret_key, message):
    h = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf8'), hashlib.sha512)
    return base64.b64encode(h.digest())


api_key = '1A905557-16C4-4E38-95B0-00D826AEF1C6'
secret_key = '72b35601a5869889a9d1af6f7d4a48da54dec86b06a06eb23fae2cd0bb4652d8'

ws = create_connection("wss://ws.gate.io/v3/")

nonce = int(time.time() * 1000)
signature = get_sign(secret_key, str(nonce))

ws.send(json.dumps({
    "id": 12312,
    "method": "server.sign",
    "params": [api_key, signature.decode(), nonce]
    }))
print(ws.recv())

# ws = create_connection("wss://ws.gateio.io/v3/")
# print(ws)
# ws.send('{"id":12312, "method":"ticker.subscribe", "params":["BTC_USDT", "EOS_USDT"]}')


# while True:
#     print(ws.recv())