import requests
import threading



def usd_get():
    try:
        data = requests.get('https://data.gateio.io/api2/1/ticker/usdt_cny', timeout=5)
        usd = data.json()['last']
        print (float(usd))
    except:
        return False
        pass


t = threading.Thread(target=usd_get)
t.start()

