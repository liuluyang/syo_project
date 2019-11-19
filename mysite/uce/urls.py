#coding:utf8

from django.urls import path
import uce.views_kuaixun as kuaixun
import uce.views_gateio as gateio
from uce import okex_futures
from uce import tradingview

urlpatterns = [
    path('market/', gateio.echo),
    path('market/kline/', gateio.echo),
    path('echo_once/', gateio.echo_once),

    path('kuaixun/', kuaixun.push_message), #快讯长连接消息推送提醒

    path('okex-futures/', okex_futures.currency_data_get),
    path('okex-futures/futures-spots-kline-all/',
         okex_futures.futures_spots_kline_get_all),
    path('okex-futures/blasting-orders-all/',
         okex_futures.blasting_orders_get_all),
    path('okex-futures/currencies/',
         okex_futures.currency_get_all),

    path('tradingview-idea', tradingview.tradingview_idea_get),
    path('remind-history', tradingview.remind_history)
 ]

