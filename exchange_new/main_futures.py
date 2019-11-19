
from multiprocessing import Pool
from utils._logger import Logger as logger

from futures.okex import OkexFutures


def error(e):
    print (e)
    logger.warn('futures子进程异常：{}'.format(e))

if __name__ == '__main__':
    server_list = [
                    OkexFutures().data_chart_main,
                    OkexFutures().price_main,
                    OkexFutures().blastingOrders_main
                   ]

    p = Pool(len(server_list))
    for m in server_list:
        p.apply_async(m, error_callback=error)
    p.close()
    p.join()
