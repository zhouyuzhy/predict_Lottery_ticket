from futu import *
from stock.db import *
from stock.db import KLineMapper


def fetch_stock_datas(stock_code, start_date, end_date):
    # 1、查询开始到结束时间DB中的数据
    kline_list = KLineMapper.query_kline(stock_code, start_date, end_date)
    # 2、如果DB中第一条时间晚于需要查询的时间，查全量api
    isAll = False
    isPartial = False
    if len(kline_list) == 0:
        isAll = True
    if len(kline_list)>0:
        isAll = kline_list[0].time_key > start_date

    # 3、如果DB中最后一条时间早于需要查询的时间，查api的时间为DB中最后一天到end_date的数据
    if len(kline_list) >0 and not isAll:
        isPartial = kline_list[-1].time_key < end_date

    if not isAll and not isPartial:
        return kline_list
    if isPartial:
        start_date = kline_list[-1].time_key
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    data_list = None
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_code, start=start_date, end=end_date,
                                                              max_count=1000)  # 每页5个，请求第一页
    if ret == RET_OK:
        data_list = data
    else:
        print('error:', data)
        raise Exception('unknown error')
    while page_req_key is not None:  # 请求后面的所有结果
        print('*************************************')
        ret, data, page_req_key = quote_ctx.request_history_kline(stock_code, start=start_date, end=end_date,
                                                                  max_count=1000,
                                                                  page_req_key=page_req_key)  # 请求翻页后的数据
        if ret == RET_OK:
            data_list = data_list.append(data, ignore_index=True)
        else:
            print('error:', data)
            raise Exception('unknown error')
    quote_ctx.close()
    data_kline_obj_list = []
    # data_list to kline_list
    for index in data_list.index:
        kline = KLine()
        kline.code = data_list['code'][index]
        kline.time_key = datetime.strptime(data_list['time_key'][index],'%Y-%m-%d %H:%M:%S')
        kline.open = data_list['open'][index]
        kline.close = data_list['close'][index]
        kline.high = data_list['high'][index]
        kline.low = data_list['low'][index]
        kline.pe_ratio = data_list['pe_ratio'][index]
        kline.turnover_rate = data_list['turnover_rate'][index]
        kline.volume = data_list['volume'][index]
        kline.turnover = data_list['turnover'][index]
        kline.change_rate = data_list['change_rate'][index]
        kline.last_close = data_list['last_close'][index]
        data_kline_obj_list.append(kline)
        KLineMapper.add_kline(kline)

    if isPartial:
        kline_list.extend(data_kline_obj_list)
    return data_list

