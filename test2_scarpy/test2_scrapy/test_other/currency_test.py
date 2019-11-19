
#coding:utf8


import pymysql
import json

class ConnectDB(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='lvjian',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True
        )

        self.cursor = self.connect.cursor()

    def find_common(self):
        sql = 'select name from uce_currency_bsj'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        num = 0
        list_many = []
        list_no = []
        for obj_name in data_obj:
            name = obj_name[0]
            sql = 'select id,name from uce_currency_fxh where name="'+name+'"'
            self.cursor.execute(sql)
            fet = self.cursor.fetchall()
            fet_n = len(fet)
            if fet_n==1:
                num+=1
            elif fet_n>1:
                list_many.append(fet)
            elif fet_n==0:
                list_no.append(name)

        print ('可以更新的：', num)
        print ('没有的:',len(list_no), list_no)
        print ('多个的：', len(list_many), list_many)



if __name__ == '__main__':
    c = ConnectDB()
    print (c.find_common())


