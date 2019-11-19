import execjs
import requests
from test2_scrapy.test.wenshu.user_agents import agents
import random
import json
from test2_scrapy.test.wenshu.docid import getkey, decode_docid

user_agent = random.choice(agents)


def vl5x_get(vjkl5):
    with open('getKey.js') as f:
        file = f.read()
        ctx = execjs.compile(file)
        vl5x = ctx.call('getKey', vjkl5)
        guid = ctx.call('getGuid')
        return vl5x, guid

#print(vl5x_get('39ac8798ff46e8c401bc1868ee6a74e4bb15af60'))

data_str = """
Param: 案件类型:刑事案件
Index: 1
Page: 10
Order: 法院层级
Direction: desc
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


headers = {
    'User-Agent':user_agent,
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
}

cookies_str = '_gscu_2116842793=45290230pz5s0i39; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545290231,1545298274,1545356434,1545716938; _gscbrs_2116842793=1; _gscs_2116842793=t457200630bgno783; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545721424; vjkl5=309398ff58e89401c818f293f25f457f06713d4a'
cookies_list = cookies_str.split(';')
cookies_dict = {}
for s in cookies_list:
    s = s.split('=')
    cookies_dict[s[0].strip()] = s[1].strip()
print(cookies_dict)

# r = requests.post('http://wenshu.court.gov.cn/List/ListContent', data=data,
#                   cookies=cookies_dict, headers=headers)

url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
r = requests.get(url, headers=headers)
vjkl5 = r.headers['Set-Cookie']
vjkl5 = vjkl5.split(';')[0].split('=')[-1].strip()
print(vjkl5)

vl5x = vl5x_get(vjkl5)
print(vl5x)

# data['vl5x'] = vl5x[0]
# data['guid'] = vl5x[1]
data['Param'] = '法院地域:北京市,中级法院:北京市第二中级人民法院'#'案件类型:刑事案件'
data['parval'] = '北京市第二中级人民法院'
#cookies_dict = {}
cookies_dict['vjkl5'] = vjkl5
print(data)
print(cookies_dict)

r = requests.post('http://wenshu.court.gov.cn/List/CourtTreeContent', data=data,
                  cookies=cookies_dict, headers=headers)

print(r.status_code)
print(r.text)

data_get = json.loads(r.json())
print(type(data_get), len(data_get))

num = 0
for d in data_get:
    for k,v in d.items():
        print(k,v)
        if k == 'Child':
            for c in v:
                print(c)
                num += c['IntValue']
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(num)