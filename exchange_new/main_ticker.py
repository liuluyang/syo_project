
from multiprocessing import Pool
from utils._logger import Logger as logger

#最新价
from markets.gateio import Market as gateio
from markets._binance import Market as binance
from markets.okex import Market as okex
from markets.huobi import Market as huobi
from markets.mysql_update import Update as update
from markets.bigone import Market as bigone
from markets.bibox import Market as bibox
from markets.zb import Market as zb


def error(e):
    print (e)
    logger.warn('exchange子进程异常：{}'.format(e))

if __name__ == '__main__':
    server_list = [
                   gateio().data_get, gateio().ticker_new,
                   binance().data_get, binance().ticker_new,
                   okex().data_get, okex().ticker_new,
                   huobi().data_get, huobi().ticker_new,
                   update().exchange_update, update().ranking_update,

                   # bigone().data_get, bigone().ticker_new,
                   bibox().data_get, bibox().ticker_new,

                   zb().data_get, zb().ticker_new,
                   ]

    p = Pool(len(server_list))
    for m in server_list:
        p.apply_async(m, error_callback=error)
    p.close()
    p.join()
