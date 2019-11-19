import execjs
import requests
from test2_scrapy.test.wenshu.user_agents import agents
import random
import json
import time

#user_agent = random.choice(agents)
with open('getKey.js') as f:
    file = f.read()
    ctx = execjs.compile(file)


def list_get(param=''):
    def vl5x_get(vjkl5):
        vl5x = ctx.call('getKey', vjkl5)
        guid = ctx.call('getGuid')
        return vl5x, guid

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

    headers = {
        'User-Agent':random.choice(agents),
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1'
    }

    cookies_str = '_gscu_2116842793=45290230pz5s0i39; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545290231,1545298274,1545356434,1545716938; _gscbrs_2116842793=1; _gscs_2116842793=t457200630bgno783; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545721424; vjkl5=309398ff58e89401c818f293f25f457f06713d4a'
    cookies_list = cookies_str.split(';')
    cookies_dict = {}
    for s in cookies_list:
        s = s.split('=')
        cookies_dict[s[0].strip()] = s[1].strip()

    url = 'http://wenshu.court.gov.cn/List/List?sorttype=1'
    r = requests.get(url, headers=headers)
    vjkl5 = r.headers['Set-Cookie']
    vjkl5 = vjkl5.split(';')[0].split('=')[-1].strip()

    vl5x = vl5x_get(vjkl5)

    data['vl5x'] = vl5x[0]
    data['guid'] = vl5x[1]
    data['Index'] = 1
    data['Page'] = 10
    data['Param'] = '裁判日期:2019-01-01 TO 2019-01-03,'+param#'案件类型:刑事案件'
    #data['Order'] = '法院层级'
    #cookies_dict = {}
    cookies_dict['vjkl5'] = vjkl5

    count = None
    try:
        r = requests.post('http://wenshu.court.gov.cn/List/ListContent', data=data,
                          cookies=cookies_dict, headers=headers)
        data_get = json.loads(r.json())
        count = data_get[0].get('Count', 0)
        return count
    except Exception as e:
        print(e)
        print(r.status_code)
        print(r.text)
        time.sleep(30)
    time.sleep(0.5)

    return count

#print(list_get())


import json

court_num = 0
with open('court.json', 'r') as f:
    data = json.load(f)
    for k_t, v_t in data.items():
        # while 1:
        #     result = list_get('法院地域:{}'.format(k_t))
        #     if result is not None:
        #         break
        print(k_t)
        for k_m, v_m in v_t.items():
            pass
            # while 1:
            #     result = list_get('中级法院:{}'.format(k_m))
            #     if result is not None:
            #         break
            print(' '*6, k_m)
            for k_b in v_m:
                pass
                print(' '*15, k_b)