#coding:utf8


import re



s = "background-image:url('" \
    "http://admin2.weilaicaijing.com/wp-content/uploads/2018/05/2018051615075128.jpg');"

print (re.search(r'http.*\'', s).group()[:-1])

date = '07月20日·星期五'

print (re.findall(r'(\d{2})',date))