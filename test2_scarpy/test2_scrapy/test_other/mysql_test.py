#coding:utf8


import pymysql
import json

class ConnectDB(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='weibo',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True
        )

        self.cursor = self.connect.cursor()

    def users_get(self):
        sql = 'select *from user'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

    def detail_get(self, blog_id):
        sql = 'select * from blog_detail where id={id}'.format(id=blog_id)
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchone()
        return data_obj

    def blog_new_get(self, nums):
        sql = 'select *from blog_detail order by created_time desc limit {nums}'.format(nums=nums)
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()
        return data_obj

    def blog_get_by_time(self, datetime):
        sql = 'select *from blog_detail where created_time>+"'+datetime+'" order by created_time desc'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()
        return data_obj

if __name__ == '__main__':
    c = ConnectDB()
    #print (c.users_get())

    # data = c.detail_get(429)
    # for i in data:
    #     print (type(i),i)
    # pic = json.loads(data[4])
    # print (type(pic), pic['pic_ids'])
    # retweet = json.loads(data[-1])
    # print (retweet)

    # data = c.blog_new_get(5)
    # for i in data:
    #     print (i[0],i[3])

    data = c.blog_get_by_time("2018-07-16 12:00:00")
    print (len(data))
    for i in data:
        print (i[0],i[3])


