
from multiprocessing import Pool
from utils._logger import Logger as logger

#预警
from early_warning.symbol_remind import Remind as remind
#from early_warning.kline_remind import RemindKline
from early_warning.kline_remind_new import RemindKline
from early_warning.kline_remind_futures import RemindKline as RemindKlineFutures
from early_warning.kline_remind_spot import RemindKline as RemindKlineSpot

def error(e):
    print (e)
    logger.warn('remind子进程异常：{}'.format(e))

if __name__ == '__main__':
    server_list = []

    server_list += [remind().main]
    #server_list += [RemindKline().main]
    server_list += [RemindKline().main]
    #server_list += [RemindKlineFutures().main]
    #server_list += [RemindKlineSpot().main]

    p = Pool(len(server_list))
    for m in server_list:
        p.apply_async(m, error_callback=error)
    p.close()
    p.join()
