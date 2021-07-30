from collections import OrderedDict
from time import sleep

from futu import *
import pandas as pd
from datetime import datetime

from stock.fetch.fetch_store import fetch_stock_datas

Market_CODE = Market.HK
COMPARE_TARGET = 'HK.800000'
START_DATE = '2021-04-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def compare(plate_k_lines, compare_k_lines):
    return (plate_k_lines[-1].close / plate_k_lines[0].open) / (
                compare_k_lines[-1].close / compare_k_lines[0].open)


if __name__ == '__main__':
    plate_compare = {}
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # code plate_name plate_id
    ret, data = quote_ctx.get_plate_list(Market_CODE,Plate.INDUSTRY)
    if ret != RET_OK:
        print('error:', data)
        raise Exception
    # 拉compare的k line
    compare_k_lines = fetch_stock_datas(COMPARE_TARGET,START_DATE, END_DATE)
    # 拉每一个版块的k line，完成对比
    i = 0
    for plate_code in data['code'].values:
        try:
            plate_k_lines = fetch_stock_datas(plate_code,START_DATE, END_DATE)
        except Exception:
            sleep(60)
            plate_k_lines = fetch_stock_datas(plate_code,START_DATE, END_DATE)
        compare_result = compare(plate_k_lines, compare_k_lines)
        plate_name = data.loc[data['code'] == plate_code]['plate_name'].values[0]
        plate_compare.update({plate_name: compare_result})
    plate_compare_descending = OrderedDict(sorted(plate_compare.items(),
                                      key=lambda item: item[1], reverse=True))
    print(plate_compare_descending)
    quote_ctx.close()