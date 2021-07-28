from collections import OrderedDict
from time import sleep

from futu import *
import pandas as pd
from datetime import datetime

Market_CODE = Market.HK
COMPARE_TARGET = 'HK.800000'
START_DATE = '2021-07-19'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def fetch_stock_datas(stock_code):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    data_list = None
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_code, start=START_DATE, end=END_DATE,
                                                              max_count=1000)  # 每页5个，请求第一页
    if ret == RET_OK:
        data_list = data
    else:
        print('error:', data)
        raise Exception('unknown error')
    while page_req_key is not None:  # 请求后面的所有结果
        print('*************************************')
        ret, data, page_req_key = quote_ctx.request_history_kline(stock_code, start=START_DATE, end=END_DATE,
                                                                  max_count=1000,
                                                                  page_req_key=page_req_key)  # 请求翻页后的数据
        if ret == RET_OK:
            data_list = data_list.append(data, ignore_index=True)
        else:
            print('error:', data)
            raise Exception('unknown error')
    quote_ctx.close()
    return data_list


def compare(plate_k_lines, compare_k_lines):
    return (plate_k_lines['close'].iloc[-1] / plate_k_lines['open'][0]) / (
                compare_k_lines['close'].iloc[-1] / compare_k_lines['open'][[0]])


if __name__ == '__main__':
    plate_compare = {}
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # code plate_name plate_id
    ret, data = quote_ctx.get_plate_list(Market_CODE,Plate.INDUSTRY)
    if ret != RET_OK:
        print('error:', data)
        raise Exception
    # 拉compare的k line
    compare_k_lines = fetch_stock_datas(COMPARE_TARGET)
    # 拉每一个版块的k line，完成对比
    i = 0
    for plate_code in data['code'].values:
        plate_k_lines = fetch_stock_datas(plate_code)
        compare_result_list = compare(plate_k_lines, compare_k_lines)
        plate_name = data.loc[data['code'] == plate_code]['plate_name'].values[0]
        plate_compare.update({plate_name: compare_result_list[0]})
        i = i+1
        if i > 58:
            i = 0
            sleep(60)
    plate_compare_descending = OrderedDict(sorted(plate_compare.items(),
                                      key=lambda item: item[1], reverse=True))
    print(plate_compare_descending)
    quote_ctx.close()