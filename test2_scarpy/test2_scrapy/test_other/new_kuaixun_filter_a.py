

import re


text = '<div><a href="baidu.com"><span></span></a><a href=""></a></div>'
print (text)

#text = text.replace(r'</a>','')

a = re.findall(r'<a.*?>', text)

#print (text)

#print (a)
for  i in a+['</a>']:
    text = text.replace(i, '')

print (text)
