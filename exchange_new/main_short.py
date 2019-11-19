
from multiprocessing import Pool
from utils._logger import Logger as logger

#短线精灵
from short_elves.gateio_kline import Kline as gateio_kline
from short_elves._binance_kline import Kline as binance_kline
from short_elves.okex_kline import Kline as okex_kline
from short_elves.huobi_kline import Kline as huobi_kline
from short_elves.bigone_kline import Kline as bigone_kline
from short_elves.bibox_kline import Kline as bibox_kline
from short_elves.zb_kline import Kline as zb_kline

from short_elves.gateio_trade import Trade as gateio_trade
from short_elves._binance_trade import Trade as binance_trade
from short_elves.okex_trade import Trade as okex_trade
from short_elves.huobi_trade import Trade as huobi_trade
from short_elves.bigone_trade import Trade as bigone_trade
from short_elves.bibox_trade import Trade as bibox_trade
from short_elves.zb_trade import Trade as zb_trade

def error(e):
    print (e)
    logger.warn('exchange子进程异常：{}'.format(e))

if __name__ == '__main__':
    server_list = []

    server_list += [gateio_kline().kline, binance_kline().kline,
                    okex_kline().kline, huobi_kline().kline]

    server_list += [gateio_trade().trade, binance_trade().trade,
                    okex_trade().trade, huobi_trade().trade]

    server_list += [# bigone_kline().kline,
                    # bigone_trade().trade
                    ]

    server_list += [bibox_kline().kline,
                    bibox_trade().trade
                    ]

    server_list += [zb_kline().kline,
                    zb_trade().trade
                    ]

    p = Pool(len(server_list))
    for m in server_list:
        p.apply_async(m, error_callback=error)
    p.close()
    p.join()
