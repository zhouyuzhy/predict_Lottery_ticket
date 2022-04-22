import webbrowser

import pandas as pd
import traceback
from datetime import datetime, timedelta
import os
from tqdm import tqdm
from collections import OrderedDict
from czsc import signals, CZSC
from czsc.objects import Signal, Factor, Event, Freq, Operate, RawBar

from stock.db.model import KLineLevel
from stock.fetch import fetch_store
from stock_trade import constant


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


def stocks_dwm_selector(codes, end_date: [str, datetime] = datetime.now().strftime('%Y-%m-%d'), kline_level=KLineLevel.K_60M):
    """大级别选股（日线&月线&周线）"""

    for symbol in codes:
        try:
            if kline_level == KLineLevel.K_DAY:
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            else:
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            datas = fetch_store.fetch_stock_datas(symbol, start_date=start_date, end_date=end_date, kline_level=kline_level)
            k0 = convert2RawBar(datas)
            c0 = CZSC(k0)

            open_in_browser(c0)
        except:
            print("fail on {}".format(symbol))
            traceback.print_exc()
    return c0


if __name__ == '__main__':
    # codes = [constant.STOCK_CODE_TENGXUN,constant.STOCK_CODE_MEITUAN,constant.STOCK_CODE_HTY]
    codes = [constant.STOCK_CODE_HTY]
    # codes= ['SZ.002157','SZ.300116',constant.STOCK_CODE_HTY]
    # codes = ['SZ.300116']
    # codes = ['SZ.002157']
    stocks_dwm_selector(codes,kline_level=KLineLevel.K_1M)
