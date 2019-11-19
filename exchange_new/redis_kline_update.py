import time
import redis
from utils._logger import Logger as logger

NOW = int(time.strftime('%H', time.localtime()))

def delete_db4():
    """
    清除短线精灵redis相关数据
    :return: 
    """
    pool = redis.ConnectionPool(host='localhost', port=6379, db=4, password='lvjian')
    r = redis.Redis(connection_pool=pool)

    if NOW == 0:
        r.delete('okex_kline')
        r.delete('okex_times')

        r.delete('huobi_kline')
        r.delete('huobi_times')

        r.delete('zb_kline')
        r.delete('zb_times')

        logger.info('零点删除成功')
    elif NOW == 8:
        r.delete('gateio_kline')
        r.delete('gateio_times')

        r.delete('binance_kline')
        r.delete('binance_times')

        r.delete('bigone_kline')
        r.delete('bigone_times')

        r.delete('bibox_kline')
        r.delete('bibox_times')

        logger.info('八点删除成功')

if __name__ == '__main__':
    delete_db4()





