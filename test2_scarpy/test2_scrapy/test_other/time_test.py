#!/usr/bin/python
import time

#时间戳转日期时间
print(time.time())
t = float(1530839713)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))

print (type(time.ctime()), time.ctime(13412))
print (time.strftime('%Y-%m-%d %X',time.strptime('Fri Jul 13 08:31:08  2018',"%a %b %d %H:%M:%S  %Y")))


#'Thu Jul 12 16:43:14 +0800 2018'
created_at = 'Fri Jul 13 08:31:08 +0800 2018'
clean_time = ''.join(created_at.split('+0800'))
created_time = time.strftime('%Y-%m-%d %X',time.strptime(clean_time,"%a %b %d %H:%M:%S  %Y"))
print (created_time)