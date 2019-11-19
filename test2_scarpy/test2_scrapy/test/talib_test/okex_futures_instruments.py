import requests
import json
import time


instruments = requests.get('https://www.okex.me/api/futures/v3/instruments').json()
print(type(instruments), instruments)

for d in instruments:
    print(d)
    symbol, instrument_id, alias = d.get('underlying_index'), d.get('instrument_id'), d.get('alias')
    print(symbol, instrument_id, alias)