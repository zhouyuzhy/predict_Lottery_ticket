from futu import *


def fetch_stock_datas(stock_code, start_date, end_date):
    # 1、查询开始到结束时间DB中的数据

    # 2、如果DB中第一条时间晚于需要查询的时间，查全量api

    # 3、如果DB中最后一条时间早于需要查询的时间，查api的时间为DB中最后一天到end_date的数据
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
    return data_list