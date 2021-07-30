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


def daily_compare(plate_k_lines, compare_k_lines):
    result = {}
    for plate_k_line in plate_k_lines:
        compare_k_line = [k_line for k_line in compare_k_lines if k_line.time_key==plate_k_line.time_key][0]
        compare_ratio = (plate_k_line.close / plate_k_line.last_close) / (
                compare_k_line.close / compare_k_line.last_close)
        result.update({plate_k_line.time_key:compare_ratio})
    return result


def daily_with_start_compare(plate_k_lines, compare_k_lines):
    result = {}
    for plate_k_line in plate_k_lines:
        compare_k_line = [k_line for k_line in compare_k_lines if k_line.time_key==plate_k_line.time_key][0]
        compare_ratio = (plate_k_line.close / plate_k_lines[0].open) / (
                compare_k_line.close / compare_k_lines[0].open)
        result.update({plate_k_line.time_key:compare_ratio})
    return result


if __name__ == '__main__':
    plate_compare = {}
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # code plate_name plate_id
    ret, data = quote_ctx.get_plate_list(Market_CODE,Plate.INDUSTRY)
    if ret != RET_OK:
        print('error:', data)
        raise Exception
    # 每日当天的涨跌幅与大盘对比
    daily_compare_list = {}
    # 每日距离开始时间的涨跌幅与大盘对比
    daily_with_start_compare_list = {}
    # 拉每一个版块的k line，与大盘对比开始到结束的涨幅
    compare_k_lines = fetch_stock_datas(COMPARE_TARGET,START_DATE, END_DATE)
    for plate_code in data['code'].values:
        try:
            plate_k_lines = fetch_stock_datas(plate_code,START_DATE, END_DATE)
        except Exception:
            sleep(60)
            plate_k_lines = fetch_stock_datas(plate_code,START_DATE, END_DATE)
        compare_result = compare(plate_k_lines, compare_k_lines)
        plate_name = data.loc[data['code'] == plate_code]['plate_name'].values[0]
        plate_compare.update({plate_name: compare_result})

        daily_compare_result = daily_compare(plate_k_lines, compare_k_lines)
        daily_compare_list.update({plate_name: daily_compare_result})

        daily_with_start_compare_result = daily_with_start_compare(plate_k_lines, compare_k_lines)
        daily_with_start_compare_list.update({plate_name: daily_with_start_compare_result})
    quote_ctx.close()
    # 对比数据输出
    plate_compare_descending = OrderedDict(sorted(plate_compare.items(),
                                      key=lambda item: item[1], reverse=True))
    print(plate_compare_descending)
    # 强于大盘的版块每日折线图
