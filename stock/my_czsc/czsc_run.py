import pandas as pd
import traceback
from datetime import datetime
import os
from tqdm import tqdm
from collections import OrderedDict
from czsc import signals, CZSC
from czsc.objects import Signal, Factor, Event, Freq, Operate, RawBar

from stock.db.model import KLineLevel
from stock.fetch import fetch_store


def convert2RawBar(klines):
    rowbars = []
    id = 0
    for kline in klines:
        id = id + 1
        rb = RawBar(kline.code, id, kline.time_key, Freq.D, float(kline.open), float(kline.close), float(kline.high), float(kline.low),
                    float(kline.volume))
        rowbars.append(rb)
    return rowbars


def stocks_dwm_selector(end_date: [str, datetime] = datetime.now().strftime('%Y-%m-%d'), data_path=None):
    """大级别选股（日线&月线&周线）"""

    codes = ['HK.01347']
    for symbol in codes:
        try:
            # k0 = ts.get_kline(symbol, asset='E', freq=Freq.D, start_date="20200101", end_date=end_date)
            # k1 = ts.get_kline(symbol, asset='E', freq=Freq.W, start_date="20100101", end_date=end_date)
            # k2 = ts.get_kline(symbol, asset='E', freq=Freq.M, start_date="20000101", end_date=end_date)
            datas = fetch_store.fetch_stock_datas(symbol, start_date="2021-01-01", end_date=end_date, kline_level=KLineLevel.K_60M)
            k0 = convert2RawBar(datas)
            c0 = CZSC(k0)
            # c1 = CZSC(k1, get_signals=signals.get_selector_signals)
            # c2 = CZSC(k2, get_signals=signals.get_selector_signals)

            c0.open_in_browser()
        except:
            print("fail on {}".format(symbol))
            traceback.print_exc()
    return c0


if __name__ == '__main__':
    stocks_dwm_selector()
