import requests


data = requests.get('https://app.blockmeta.com/w1/news/list?num=20&page=1&cat_id=572').json()


print (data)

data_list = data['list']
for num, obj in enumerate(data_list):
    print (num, obj)
    for k,v in obj.items():
        print (k, v)
print ('```````````````````````````')
# list_new = sorted(data_list, key=lambda obj:obj['id'], reverse=True)
# for num, obj in enumerate(list_new):
#     print (num, obj)
key_name = ['id', 'post_date_format', 'title', 'desc', 'image', 'author_info/display_name']