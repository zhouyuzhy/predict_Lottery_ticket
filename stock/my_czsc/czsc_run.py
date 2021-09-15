import webbrowser

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


def open_in_browser(c0):
    home_path = os.path.expanduser("~")
    file_html = os.path.join(home_path, "temp_czsc.html")
    chart = c0.to_echarts()
    chart.render(file_html)
    webbrowser.open('file://' +os.path.realpath(file_html))


def stocks_dwm_selector(codes, end_date: [str, datetime] = datetime.now().strftime('%Y-%m-%d')):
    """大级别选股（日线&月线&周线）"""

    for symbol in codes:
        try:
            datas = fetch_store.fetch_stock_datas(symbol, start_date="2021-01-01", end_date=end_date, kline_level=KLineLevel.K_60M)
            k0 = convert2RawBar(datas)
            c0 = CZSC(k0)

            open_in_browser(c0)
        except:
            print("fail on {}".format(symbol))
            traceback.print_exc()
    return c0


if __name__ == '__main__':
    codes = ['HK.01347', 'HK.02359', 'HK.09633']
    stocks_dwm_selector(codes)
