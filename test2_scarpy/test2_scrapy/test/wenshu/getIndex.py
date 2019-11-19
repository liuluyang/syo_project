import requests
from test2_scrapy.test.wenshu.vl5x import getvjkl5

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
}
url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
r = requests.get(url, headers=headers)

print(r.status_code)
print(r.headers)
print(r.cookies.items())
vjk = r.headers['Set-Cookie']
vjk = vjk.split(';')[0].split('=')[-1].strip()
print(vjk)
try:
    print(getvjkl5(vjk))
except:
    pass

"""
39ac8798ff46e8c401bc1868ee6a74e4bb15af60
3181e7fedeef2cfee70f6aa7
"""