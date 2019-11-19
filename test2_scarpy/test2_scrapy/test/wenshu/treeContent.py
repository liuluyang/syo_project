import execjs
import requests
from test2_scrapy.test.wenshu.user_agents import agents
import random
import json
import time
import copy
from test2_scrapy.test.wenshu.docid import getkey, decode_docid

#user_agent = random.choice(agents)
with open('getKey.js') as f:
    file = f.read()
    ctx = execjs.compile(file)

def getCourtTree(url='http://wenshu.court.gov.cn/List/TreeContent', **param):
    def vl5x_get(vjkl5):
        vl5x = ctx.call('getKey', vjkl5)
        guid = ctx.call('getGuid')
        return vl5x, guid

    headers = {
        'User-Agent':random.choice(agents),
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer':'http://wenshu.court.gov.cn/list/list/?sorttype=1'
    }
    #get cookies
    url_cookies = 'http://wenshu.court.gov.cn/list/list/?sorttype=1'
    r = requests.get(url_cookies, headers=headers)
    vjkl5 = r.headers['Set-Cookie']
    vjkl5 = vjkl5.split(';')[0].split('=')[-1].strip()
    #make vl5x
    vl5x = vl5x_get(vjkl5)
    #form data
    data = {}
    data['vl5x'] = vl5x[0]
    data['guid'] = vl5x[1]
    #data['Param'] = param
    data.update(param)
    #make cookies
    cookies = {}
    cookies['vjkl5'] = vjkl5

    r = requests.post(url, data=data,
                      cookies=cookies, headers=headers)
    time.sleep(0.5)
    try:
        data_get = json.loads(r.json())

        return data_get
    except Exception as e:
        print(e)
        return

first_court = {}
data_get = getCourtTree(Param='')
for first in data_get:
    if first['Key'] == '法院地域':
        for key,values in first.items():
            if key == 'Child':
                for v in values:
                    if not v['parent']:
                        first_court[v['Key']] = {}

print(len(first_court), first_court)

# for court_name in list(first_court.keys()):
#     print(court_name)
#     data = getCourtTree('http://wenshu.court.gov.cn/List/CourtTreeContent',
#                         Param='法院地域:{}'.format(court_name), parval=court_name
#                         )
#     print(court_name, data)
#     if not data:
#         continue
#     for d in data[0]['Child']:
#         if '...' not in d['Value']:
#             print(d)
#             first_court[court_name][d['Key']] = []
#             data_b = getCourtTree(
#                 'http://wenshu.court.gov.cn/List/CourtTreeContent',
#                 Param='中级法院:{}'.format(d['Key']), parval=d['Key']
#                 )
#             if not data_b:
#                 continue
#             court_list = []
#             for d_b in data_b[0]['Child']:
#                 if '...' not in d['Value']:
#                     print(d_b)
#                     court_list.append(d_b['Key'])
#             first_court[court_name][d['Key']] = court_list
#             with open('court.json', 'w', encoding='utf8') as file:
#                 json.dump(first_court, file)
#         print(first_court)
#     time.sleep(1)
