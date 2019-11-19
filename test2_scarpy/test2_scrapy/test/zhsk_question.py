import requests
import time

# cookies = "__jsluid=a8a60d9cf263cfe27b54f36333193e22; " \
#           "qa_cnki_net_uid=dd26a84c-6f33-7df0-f7ef-7d38ad94ff3d; " \
#           "Hm_lvt_3638a62525c09282e5cd18863d8f4456=1543998462; " \
#           "Hm_lpvt_3638a62525c09282e5cd18863d8f4456=1543999504"
start = int(time.time())
next = start + 18*60
cookies = {
    "__jsluid":"a8a60d9cf263cfe27b54f36333193e22",
    "qa_cnki_net_uid":"dd26a84c-6f33-7df0-f7ef-7d38ad94ff3d",
    "Hm_lvt_3638a62525c09282e5cd18863d8f4456":str(start),
    "Hm_lpvt_3638a62525c09282e5cd18863d8f4456":str(next)
}

print(cookies)

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
data = {
            'rid':'1/41;1/50',
            'pagesize':1000,
            'pageindex':1
        }
q_list = requests.post('http://zhsk.12348.gov.cn/qa.web/query/GetLb',
                       headers=headers,
                       data=data).json()
print(q_list)
print(len(q_list['list']))


with open('测试.text', 'w+') as f:
    base_url = 'http://zhsk.12348.gov.cn/qa.web/query/detail?id='
    for q in q_list['list']:
        print(q['id'])
        f.write(base_url+q['id']+'\n')