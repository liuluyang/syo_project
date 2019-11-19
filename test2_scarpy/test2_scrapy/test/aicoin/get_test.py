import requests
import json


header = {
'Origin': 'https://www.aicoin.net.cn',
'Referer': 'https://www.aicoin.net.cn/chart/okex-eosquarter',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url_get = 'https://assets-www.aicoin.net.cn/beta-v19/static/alert.ogg'
r = requests.get(url_get, headers=header)

print(r)
print(r.headers)
for k,v in r.headers.items():
    print(k,'````````````' ,v)
#print(r.json())