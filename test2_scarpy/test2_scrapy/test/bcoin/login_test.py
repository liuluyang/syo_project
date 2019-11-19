import requests
import json

post_data = {
    "phone": "15076157670",
    #"areaCode": "86",
    "password": "888123"
}
post_data = json.dumps(post_data)
login_url = 'https://blz.bicoin.com.cn/user/login'
r = requests.post(login_url, data=post_data)
print(r.status_code)
print(r.json())
print(r.headers)

token = r.headers['token']
print('token:', token)

data_list = requests.get('https://blz.bicoin.com.cn/settingFirmOffer/getUserLeaderList?'
                 'pageNum=1&pageSize=10&showType=1&typeStr=97', headers={'token':token})


print(data_list.status_code)
data = data_list.json()
print('data:', data)
for d in data['data']['firmOfferHisList']:
    print(d)
    content = d['contentHtml'].split('【')[-1].split('】')[0]
    print(d['sym'], d['labelSub'], d['unit'], content, d['informTime'], d['exch'])
