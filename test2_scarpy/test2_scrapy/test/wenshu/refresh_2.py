import requests
import execjs
from test2_scrapy.test.wenshu.user_agents import agents
import random

def vl5x_get(vjkl5):
    with open('getKey.js') as f:
        file = f.read()
        ctx = execjs.compile(file)
        vl5x = ctx.call('getKey', vjkl5)
        guid = ctx.call('getGuid')
        return vl5x, guid

headers_str = """
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 237
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: _gscu_125736681=458098748hyejw25; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545810181; _gscu_2116842793=45809597se3fzm39; _gscbrs_2116842793=1; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545811609; vjkl5={};_gscs_2116842793=458101828idex041
Host: wenshu.court.gov.cn
Origin: http://wenshu.court.gov.cn
Referer: http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36
X-Requested-With: XMLHttpRequest
"""
headers_list = headers_str.split('\n')[1:-1]
headers = {}
for d in headers_list:
    d = d.split(':')
    headers[d[0].strip()] = d[1].strip()
print(headers)

data_str = """
Param: 案件类型:刑事案件
Index: 1
Page: 10
Order: 法院层级
Direction: asc
vl5x: 25b27644ca6e55fce16b67f1
number: wens
guid: e1bde4ee-d93d-8ab11c07-3270e765b2d9
"""
data_list = data_str.split('\n')[1:-1]
data = {}
for d in data_list:
    d = d.split(':')
    data[d[0].strip()] = d[1].strip()
print(data)
headers_simple = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
}
url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
r = requests.get(url, headers=headers_simple)
vjkl5 = r.headers['Set-Cookie']
vjkl5 = vjkl5.split(';')[0].split('=')[-1].strip()
print(vjkl5)

vl5x = vl5x_get(vjkl5)
print(vl5x)

data['vl5x'] = vl5x[0]
data['guid'] = vl5x[1]
headers['Cookie'] = headers['Cookie'].format(vjkl5)
headers['Cookie'] += '|pv:5'
print(data)
print(headers)

# r = requests.post('http://wenshu.court.gov.cn/Index/GetAllCountRefresh?refresh=Refresh',
#                   data=data, headers=headers
#                   )
#
# print(r.status_code)
# print(r.json())

r = requests.post('http://wenshu.court.gov.cn/List/ListContent',
                  data=data, headers=headers
                  )

print(r.status_code)
print(r.json())
print(random.choice(agents))