import requests
import json


headers = {
'x-xsrf-token': 'eyJpdiI6IlwvR3IwVGJETU0rS1kzUXRCN3E1RjVBPT0iLCJ2YWx1ZSI6IldITGIzUUM0a21KS1RucmIzZVpvQmZvSWQ3OVRjYzRsVnBJRkszQXJrcE8yZ0ZIWXF1cVV4U0VOUFhwd1oweGQ3cW5oMHNqU0oxcDBVZ2o2NCthM0RRPT0iLCJtYWMiOiJkNDdhYjNiMmRhMmRlY2ViMTI5N2UzNzhlNDRkYjgwMjI3OTJjMzE4MDY3YWIzOWZhZTZhNzdiODZhNDFlMTk5In0=',
'cookie': '_ga=GA1.3.727402005.1547436209; acw_tc=784e2c9015530617058241920e12b96d11cef01407b78228097d3c3f166d6e; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1553061714,1553667779; _pk_ref.2.cac6=%5B%22%22%2C%22%22%2C1553667780%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DUq8F7HzayNAhvbnkWzTr2bzyqdRLXYyVnCT6zQyQVDG%26wd%3D%26eqid%3Dc4bab747000a4ea6000000045c9b16b6%22%5D; _pk_ses.2.cac6=1; _gid=GA1.3.1542540282.1553667780; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1553668132; _pk_id.2.cac6=8252c0f4cda94250.1553061715.2.1553668133.1553667779.; XSRF-TOKEN=eyJpdiI6IlwvR3IwVGJETU0rS1kzUXRCN3E1RjVBPT0iLCJ2YWx1ZSI6IldITGIzUUM0a21KS1RucmIzZVpvQmZvSWQ3OVRjYzRsVnBJRkszQXJrcE8yZ0ZIWXF1cVV4U0VOUFhwd1oweGQ3cW5oMHNqU0oxcDBVZ2o2NCthM0RRPT0iLCJtYWMiOiJkNDdhYjNiMmRhMmRlY2ViMTI5N2UzNzhlNDRkYjgwMjI3OTJjMzE4MDY3YWIzOWZhZTZhNzdiODZhNDFlMTk5In0%3D; aicoin_session=eyJpdiI6InNzQk1ibGZMSmFvb0QwVEkyZ1NOUkE9PSIsInZhbHVlIjoiVG93U01PXC9Ub0I0QnViZXVmV0dFKzArblFZVTlyR0htOGt0aG9KYmpHTDJoOXVpdm1FTDhndFJ2eVo0dWwxdGd1bWNsM0tBUzhBckI5cm5qcHFVQWZnPT0iLCJtYWMiOiJmNmZiMTM0YWY5ZTI4NTU4NTUwY2JkZDFkOTI3OWViOTIxZTQ3MWE0YjZjZjZkZGM3ZWE2ZTM4ZjE1MjhiYjI3In0%3D',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'x-requested-with': 'XMLHttpReques',
}

form_data = {
'symbol': 'eosquarter:okex',
'period': 3,
'open_time': 24
}
#form_data = json.dumps(form_data)
url_post = 'https://www.aicoin.net.cn/api/chart/kline/data/period'
r = requests.post(url_post, data=form_data, headers=headers)

print(r.status_code)
print(r)