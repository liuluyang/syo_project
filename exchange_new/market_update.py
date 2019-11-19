
from markets.gateio import Market as gateio
from markets._binance import Market as binance
from markets.okex import Market as okex
from markets.huobi import Market as huobi

from markets.bibox import Market as bibox
from markets.zb import Market as zb

def market_update():
    market_list = [gateio, binance, okex, huobi, bibox, zb]
    for m in market_list:
        m().market_update()

def symbols_check():
    market_list = [gateio, binance, okex, huobi, bibox, zb]
    for m in market_list:
        m().symbols_check()


if __name__ == '__main__':
    #market_update()
    symbols_check()
    pass

