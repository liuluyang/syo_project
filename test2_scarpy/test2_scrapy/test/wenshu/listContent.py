import requests
import random

cookies_str = '_gscu_2116842793=45290230pz5s0i39; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545290231,1545298274,1545356434,1545716938; _gscbrs_2116842793=1; _gscs_2116842793=t457200630bgno783; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545721424; vjkl5=309398ff58e89401c818f293f25f457f06713d4a'
cookies_list = cookies_str.split(';')
#print(cookies_list)
cookies_dict = {}
for s in cookies_list:
    s = s.split('=')
    #print(s[0].strip())
    cookies_dict[s[0].strip()] = s[1].strip()
print(cookies_dict)

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
#print(data_list)
data = {}
for d in data_list:
    d = d.split(':')
    #print(d)
    data[d[0].strip()] = d[1].strip()
print(data)

headers_str = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
}
r = requests.post('http://wenshu.court.gov.cn/List/ListContent', data=data,
                  cookies=cookies_dict, headers=headers)

print(r.status_code)
print(r.json())


# guid = hex(int(random.random() + 1)*0x10000)[3:] + hex(int(random.random() + 1)*0x10000)
# print(guid)
data_2 = {
    'guid':'4a4512d5-c7df-de6799cf-0cfda1a9e003'
}

getcode = requests.post('http://wenshu.court.gov.cn/ValiCode/GetCode', headers=headers,
                        data=data_2
                        )
print(getcode.status_code)
print(getcode.text)