from websocket import create_connection
import time
import threading
import json
import random

#ws = create_connection("wss://ws.gateio.io/v3/")
ws_list = [create_connection("wss://ws.gateio.io/v3/") for i in range(10)]


def send(ws, data, m, num):
    #time.sleep(0.01)
    ws.send(data)
    print(num, m, ws.recv())

markets = ["BTC_USDT","BCH_USDT","ETH_USDT","ETC_USDT","QTUM_USDT","LTC_USDT","DASH_USDT","ZEC_USDT","BTM_USDT","EOS_USDT","REQ_USDT","SNT_USDT","OMG_USDT","PAY_USDT","CVC_USDT","ZRX_USDT","TNT_USDT","XMR_USDT","XRP_USDT","DOGE_USDT","BAT_USDT","PST_USDT","BTG_USDT","DPY_USDT","LRC_USDT","STORJ_USDT","RDN_USDT","STX_USDT","KNC_USDT","LINK_USDT","CDT_USDT","AE_USDT","AE_ETH","AE_BTC","CDT_ETH","RDN_ETH","STX_ETH","KNC_ETH","LINK_ETH","REQ_ETH","RCN_ETH","TRX_ETH","ARN_ETH","KICK_ETH","BNT_ETH","VET_ETH","MCO_ETH","FUN_ETH","DATA_ETH","RLC_ETH","RLC_USDT","ZSC_ETH","WINGS_ETH","MDA_ETH","RCN_USDT","TRX_USDT","KICK_USDT","VET_USDT","MCO_USDT","FUN_USDT","DATA_USDT","ZSC_USDT","MDA_USDT","XTZ_USDT","XTZ_BTC","XTZ_ETH","GNT_USDT","GNT_ETH","GEM_USDT","GEM_ETH","RFR_USDT","RFR_ETH","DADI_USDT","DADI_ETH","ABT_USDT","ABT_ETH","LEDU_BTC","LEDU_ETH","OST_USDT","OST_ETH","XLM_USDT","XLM_ETH","XLM_BTC","MOBI_USDT","MOBI_ETH","MOBI_BTC","OCN_USDT","OCN_ETH","OCN_BTC","ZPT_USDT","ZPT_ETH","ZPT_BTC","COFI_USDT","COFI_ETH","JNT_USDT","JNT_ETH","JNT_BTC","BLZ_USDT","BLZ_ETH","GXS_USDT","GXS_BTC","MTN_USDT","MTN_ETH","RUFF_USDT","RUFF_ETH","RUFF_BTC","TNC_USDT","TNC_ETH","TNC_BTC","ZIL_USDT","ZIL_ETH","TIO_USDT","TIO_ETH","BTO_USDT","BTO_ETH","THETA_USDT","THETA_ETH","DDD_USDT","DDD_ETH","DDD_BTC","MKR_USDT","MKR_ETH","DAI_USDT","SMT_USDT","SMT_ETH","MDT_USDT","MDT_ETH","MDT_BTC","MANA_USDT","MANA_ETH","LUN_USDT","LUN_ETH","SALT_USDT","SALT_ETH","FUEL_USDT","FUEL_ETH","ELF_USDT","ELF_ETH","DRGN_USDT","DRGN_ETH","GTC_USDT","GTC_ETH","GTC_BTC","QLC_USDT","QLC_BTC","QLC_ETH","DBC_USDT","DBC_BTC","DBC_ETH","BNTY_USDT","BNTY_ETH","LEND_USDT","LEND_ETH","ICX_USDT","ICX_ETH","BTF_USDT","BTF_BTC","ADA_USDT","ADA_BTC","LSK_USDT","LSK_BTC","WAVES_USDT","WAVES_BTC","BIFI_USDT","BIFI_BTC","MDS_ETH","MDS_USDT","DGD_USDT","DGD_ETH","QASH_USDT","QASH_ETH","QASH_BTC","POWR_USDT","POWR_ETH","POWR_BTC","FIL_USDT","BCD_USDT","BCD_BTC","SBTC_USDT","SBTC_BTC","GOD_USDT","GOD_BTC","BCX_USDT","BCX_BTC","HSR_USDT","HSR_BTC","HSR_ETH","QSP_USDT","QSP_ETH","INK_BTC","INK_USDT","INK_ETH","INK_QTUM","MED_QTUM","MED_ETH","MED_USDT","BOT_QTUM","BOT_USDT","BOT_ETH","QBT_QTUM","QBT_ETH","QBT_USDT","TSL_QTUM","TSL_USDT","GNX_USDT","GNX_ETH","NEO_USDT","GAS_USDT","NEO_BTC","GAS_BTC","IOTA_USDT","IOTA_BTC","NAS_USDT","NAS_ETH","NAS_BTC","ETH_BTC","ETC_BTC","ETC_ETH","ZEC_BTC","DASH_BTC","LTC_BTC","BCH_BTC","BTG_BTC","QTUM_BTC","QTUM_ETH","XRP_BTC","DOGE_BTC","XMR_BTC","ZRX_BTC","ZRX_ETH","DNT_ETH","DPY_ETH","OAX_ETH","REP_ETH","LRC_ETH","LRC_BTC","PST_ETH","BCDN_ETH","BCDN_USDT","TNT_ETH","SNT_ETH","SNT_BTC","BTM_ETH","BTM_BTC","LLT_ETH","SNET_ETH","SNET_USDT","LLT_SNET","OMG_ETH","OMG_BTC","PAY_ETH","PAY_BTC","BAT_ETH","BAT_BTC","CVC_ETH","STORJ_ETH","STORJ_BTC","EOS_ETH","EOS_BTC","BTS_USDT","BTS_BTC","TIPS_ETH","BU_USDT","BU_ETH","BU_BTC","XMC_USDT","XMC_BTC","PPS_USDT","BOE_ETH","BOE_USDT","PLY_ETH","MEDX_USDT","MEDX_ETH","CS_ETH","CS_USDT","MAN_ETH","MAN_USDT","REM_ETH","REM_USDT","LYM_ETH","LYM_BTC","LYM_USDT","ONT_ETH","ONT_USDT","BFT_ETH","BFT_USDT","IHT_ETH","IHT_USDT","SENC_ETH","SENC_USDT","TOMO_ETH","TOMO_USDT","ELEC_ETH","ELEC_USDT","HAV_ETH","HAV_USDT","SWTH_ETH","SWTH_USDT","NKN_ETH","NKN_USDT","SOUL_ETH","SOUL_USDT","LRN_ETH","LRN_USDT","EOSDAC_ETH","EOSDAC_USDT","ADD_ETH","IQ_ETH","MEETONE_ETH","DOCK_USDT","DOCK_ETH","GSE_USDT","GSE_ETH","RATING_USDT","RATING_ETH","HSC_USDT","HSC_ETH","HIT_USDT","HIT_ETH","DX_USDT","DX_ETH","GARD_USDT","GARD_ETH","FTI_USDT","FTI_ETH","SOP_ETH","SOP_USDT","LEMO_USDT","LEMO_ETH","EON_ETH","NPXS_ETH","QKC_USDT","QKC_ETH","IOTX_USDT","IOTX_ETH","RED_USDT","RED_ETH","LBA_USDT","LBA_ETH","OPEN_USDT","OPEN_ETH","MITH_USDT","MITH_ETH","SKM_USDT","SKM_ETH","XVG_USDT","XVG_BTC","NANO_USDT","NANO_BTC","NBAI_ETH","UPP_ETH","ATMI_ETH","TMT_ETH","HT_USDT","BNB_USDT","BBK_ETH","EDR_ETH","MET_ETH","MET_USDT","TCT_ETH","TCT_USDT"]

#print (len(markets))
while True:
    print(time.time())
    index = 0
    for num,m in enumerate(markets):
        data_send = {'id': 1111, 'method': 'ticker.query', 'params': None}
        data_send['params'] = [m, 86400]
        data_send = json.dumps(data_send)
        ws = ws_list[index]
        t = threading.Thread(target=send, args=(ws, data_send, m, num))
        t.start()
        index+=1
        if index==10:
            index = 0

        time.sleep(0.02)
    print(time.time())
    time.sleep(10)