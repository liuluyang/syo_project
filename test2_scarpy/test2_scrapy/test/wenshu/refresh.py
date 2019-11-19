import requests

headers_str = """
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Content-Length: 0
Cookie: _gscu_2116842793=45290230pz5s0i39; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1545356434,1545716938,1545787454,1545808024; _gscbrs_2116842793=1; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1545808073; _gscs_2116842793=458080243ewo5q39
Host: wenshu.court.gov.cn
Origin: http://wenshu.court.gov.cn
Proxy-Connection: keep-alive
Referer: http://wenshu.court.gov.cn/
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36
X-Requested-With: XMLHttpRequest
"""
headers_list = headers_str.split('\n')[1:-1]
headers = {}
for d in headers_list:
    d = d.split(':')
    headers[d[0].strip()] = d[1].strip()
print(headers)

data = {
    'refresh':'Refresh'
}

r = requests.post('http://wenshu.court.gov.cn/Index/GetAllCountRefresh?refresh=Refresh',
                  data=data, headers=headers
                  )

print(r.status_code)
print(r.json())