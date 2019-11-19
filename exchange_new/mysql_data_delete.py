import pymysql
import time
from settings import MYSQL_PRO, MYSQL_TES, IS_TEST
from utils._logger import Logger as logger

#IS_TEST = True
class DataDelete(object):

    def __init__(self):
        pass

    def mysql_obj_get(self):
        """
        连接数据库
        :return: 
        """
        MYSQL = MYSQL_TES if IS_TEST else MYSQL_PRO
        self.connect = pymysql.connect(**MYSQL)
        self.cursor = self.connect.cursor()

    def short_elves_delete(self):
        six_hour_befor = time.strftime('%Y-%m-%d %X', time.localtime(time.time()-3600*6))
        try:
            self.mysql_obj_get()
            num = self.cursor.execute(
                """
                delete from uce_short_elves where created_at<%s
                """,
                six_hour_befor
            )
            self.connect.commit()
            self.connect.close()
            logger.info('short_elves数据定时删除成功 num:{}条'.format(num))
        except Exception as e:
            logger.warning('short_elves数据定时删除失败 {}'.format(e))

    def uce_token_address_detail_delete(self):
        one_month_befor = time.strftime('%Y-%m-%d %X', time.localtime(time.time()-3600*24*31))
        try:
            self.mysql_obj_get()
            num = self.cursor.execute(
                """
                delete from uce_token_address_detail where created_at<%s
                """,
                one_month_befor
            )
            self.connect.commit()
            self.connect.close()
            logger.info('uce_token_address_detail数据定时删除成功 num:{}条'.format(num))
        except Exception as e:
            logger.warning('uce_token_address_detail数据定时删除失败 {}'.format(e))

    def uce_token_address_detail_delete_part(self):
        """
        分批删除
        :return: 
        """
        self.mysql_obj_get()
        start = time.time()
        times = 0
        while True:
            times +=1
            try:
                self.cursor.execute(
                    """
                    select *from uce_token_address_detail order by id limit 1
                    """
                )
                first_one = self.cursor.fetchone()
                id ,created_at = first_one[0], str(first_one[-1])
                created_at = time.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                one_month_befor = time.localtime(time.time() - 3600 * 24 * 31)
                #print(id, created_at)
                is_delete = one_month_befor > created_at
                if is_delete:
                    num = self.cursor.execute(
                        """
                        delete from uce_token_address_detail where id<%s
                        """,
                        id+500000
                    )
                    self.connect.commit()
                    #print('删除成功 num:{}条'.format(num))
                    logger.warning(
                        'uce_token_address_detail数据定时删除成功 num:{}条'.format(num))
                else:
                    break
                time.sleep(2)
            except Exception as e:
                logger.error('uce_token_address_detail数据定时删除失败 {}'.format(e))
                break
        used_time = time.time() - start - times*2
        logger.warning(
            'uce_token_address_detail数据定时删除成功 用时:{}s'.format(used_time))


if __name__ == '__main__':
    d = DataDelete()
    d.short_elves_delete()
    d.uce_token_address_detail_delete_part()


