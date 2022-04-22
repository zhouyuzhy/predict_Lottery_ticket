from collections import OrderedDict
from time import sleep

from futu import *

from stock.fetch.fetch_store import fetch_stock_datas
from pylab import *
import datetime


# mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


Market_CODE_HK = Market.HK
COMPARE_TARGET_HK = 'HK.800000'

Market_CODE_SH = Market.SH
COMPARE_TARGET_SH = 'SH.000001'

Market_CODE_SZ = Market.SZ
COMPARE_TARGET_SZ = 'SZ.399001'

START_DATE = '2021-07-26'
END_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


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


def compare_all_processor(market=Market_CODE_HK, compare_code=COMPARE_TARGET_HK, start_date=START_DATE, end_date=END_DATE, top_N = 9, reverse=True):
    plate_compare = {}
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # code plate_name plate_id
    ret, data = quote_ctx.get_plate_list(market, Plate.INDUSTRY)
    if ret != RET_OK:
        print('error:', data)
        raise Exception
    # 每日当天的涨跌幅与大盘对比
    daily_compare_list = {}
    # 每日距离开始时间的涨跌幅与大盘对比
    daily_with_start_compare_list = {}
    # 拉每一个版块的k line，与大盘对比开始到结束的涨幅
    compare_k_lines = fetch_stock_datas(compare_code, start_date, end_date)
    for plate_code in data['code'].values:
        try:
            plate_k_lines = fetch_stock_datas(plate_code, start_date, end_date)
        except Exception:
            sleep(60)
            plate_k_lines = fetch_stock_datas(plate_code, start_date, end_date)
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
                                                  key=lambda item: item[1], reverse=reverse))
    print(plate_compare_descending)
    # 强于大盘的版块每日折线图
    n = 0
    plt.figure()
    for plate_name in plate_compare_descending.keys():
        daily_with_start_compare_result = daily_with_start_compare_list[plate_name]
        x = daily_with_start_compare_result.keys()
        y = daily_with_start_compare_result.values()
        plt.title(market, fontsize='large', fontweight = 'bold')
        plt.plot(x, y, label=plate_name)
        plt.legend()  # 让图例生效
        n = n + 1
        if n > top_N - 1:
            break
    print('总共' + str(n) + '种展示')


if __name__ == '__main__':
    plt.ion()
    # start_date = '2021-08-09'
    # end_date = '2021-08-15'
    start_date = (datetime.datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    end_date = END_DATE
    top_N = 15
    reverse = True
    compare_all_processor(Market_CODE_HK, COMPARE_TARGET_HK, start_date, end_date, top_N, reverse)
    # compare_all_processor(Market_CODE_SH, COMPARE_TARGET_SH, start_date, end_date, top_N, reverse)
    plt.ioff()
    plt.show()


