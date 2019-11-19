#coding:utf8

import json

data = '{"name":"liu", "sex":"man", "sex":"man"}'
print (json.loads(data))

with open('loads_test.json', 'r', encoding='utf8') as f:
    print (json.load(f))

print (json.dumps({'a':[1,2,3,4]}))