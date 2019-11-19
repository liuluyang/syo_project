# coding:utf8
import sys
sys.path.append('/root/test_scrapy/test_scrapy')
import pymysql
from test_scrapy import settings


class ConnectDB(object):
    def __init__(self):
        self.connect = pymysql.connect(**settings.MYSQL)
        self.cursor = self.connect.cursor()

        # self.connect_test = pymysql.connect(**settings.MYSQL_TEST)
        # self.cursor_test = self.connect_test.cursor()

    def authors_get(self, parent_id):
        """
        获取将要抓取的微博 推特用户数据
        :param parent_id: int 内容分类标识
        :return: 
        """
        sql = 'select id,author,uuid,group_id from uce_spider_weibott where ' \
              'group_id={id}'.format(id=parent_id)
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

    def media_get(self):
        """
        获取有视频链接的微博信息
        :return: 
        """
        sql = 'select id,author,from_url from uce_spider_guanzhu where ' \
              'media_url is not Null'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

    def token_get(self):
        """
        获取代币信息
        :return: 
        """
        #测试数据库
        #self.cursor = self.cursor_test

        sql = 'select token from uce_token'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

    def update_uce_coin(self):
        """
        更新币种contract(合约) decimals(小数点)
        :return: 
        """
        #测试数据库
        #self.cursor, self.connect = self.cursor_test, self.connect_test

        import time
        sql = 'select name,token,decimal_point from uce_token group by name ' \
              'order by id'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()
        for data in data_obj:
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            self.cursor.execute(
                """
                update uce_coin set contract=%s, decimals=%s, updated_at=%s where name=%s
                """,
                (
                    data[1],
                    data[2],
                    updated_at,
                    data[0]
                )
            )
        self.connect.commit()

    def address_market_get(self):
        """
        获取钱包地址跟交易所有关联的代币信息
        :return: 
        """
        #测试数据库
        #self.cursor = self.cursor_test

        sql = 'select panking, address, market, token from uce_token_address ' \
              'where market is not NULL'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

    def device_token_get(self):
        """
        获取用户device_token
        :return: 
        """
        sql = 'select device_token from uce_sys_device'
        self.cursor.execute(sql)
        data_obj = self.cursor.fetchall()

        return data_obj

if __name__ == '__main__':
    c = ConnectDB()
    # for obj in c.authors_get(4):
    #     print(obj)
    # for obj in c.token_get():
    #     print (obj)
    #c.update_uce_coin()
    # for obj in c.address_market_get():
    #     print (obj)
    print(c.device_token_get())

