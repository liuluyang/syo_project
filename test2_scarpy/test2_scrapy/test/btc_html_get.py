import requests

# cookies = {
#     'CNZZDATA5934906':'cnzz_eid%3D1199864171-1536123834-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1539314155',
#     'QINGCLOUDELB':'77c3049cba06f2ff9eecd0cb08d409c06fec6658848c7be4d258fbc5a627439a|W8AZI|W8AXv',
#     'UM_distinctid':'165a862c32563b-0c2648747c4f9e-4446062d-13c680-165a862c32636a',
#     'eCM1_5408_smile':'2D1',
#     'yd_cookie':'1a68edd8-d552-42580e4e0fe09c56ab1dab14bc11f92c2228'
# }

cookies = {
    'BAIDUID':'C630BDAEEC6D2B9FC7EFF2E7E775695A:FG=1',
    'CNZZDATA5934906':'cnzz_eid%3D1274645067-1539324651-%26ntime%3D1539324651',
    'QINGCLOUDELB':'77c3049cba06f2ff9eecd0cb08d409c06fec6658848c7be4d258fbc5a627439a|W8BFF|W8BE1',
    'UM_distinctid':'166670ce65b16e-0b0d330922126f-4446062d-13c680-166670ce65c2dd',
    'atpsida':'808c5089ed029df5bf33b2ed_1539327251_5',
    'cna':'yjJHFKzfoSUCAXzs8vvg7IAq',
    'sca':'c61e8107'
}
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
#                         '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
#            'Accept':'application/json, text/plain, */*',
#            'Origin':'https://www.8btc.com'}
headers = {
    'Host': 'www.8btc.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

data = requests.get('https://m.8btc.com/article/289069')

print (data.status_code)
print (data.content.decode())
print (data.cookies.items())