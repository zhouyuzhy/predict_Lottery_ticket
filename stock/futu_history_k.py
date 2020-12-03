from futu import *
import pandas as pd
from datetime import datetime

STOCK_CODE_MEITUAN = 'HK.03690'

STOCK_CODE_TENGXUN = 'HK.00700'

STOCK_CODE_BABA = 'HK.09988'

STOCK_CODE_MI = 'HK.01810'

STOCK_CODE_HENGSHENG = 'HK.800000'

STOCK_CODES = [STOCK_CODE_MEITUAN, STOCK_CODE_TENGXUN, STOCK_CODE_BABA, STOCK_CODE_MI, STOCK_CODE_HENGSHENG]

START_DATE = '2017-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def fetch_stock_datas():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_history_kl_quota(get_detail=True)  # 设置True代表需要返回详细的拉取历史K 线的记录
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
    for STOCK_CODE in STOCK_CODES:
        ret, data, page_req_key = quote_ctx.request_history_kline(STOCK_CODE, start=START_DATE, end=END_DATE,
                                                                  max_count=1000)  # 每页5个，请求第一页
        if ret == RET_OK:
            print(data)
            print(data['code'][0])  # 取第一条的股票代码
            print(data['close'].values.tolist())  # 第一页收盘价转为list
        else:
            print('error:', data)
        data_list = []
        while page_req_key is not None:  # 请求后面的所有结果
            print('*************************************')
            ret, data, page_req_key = quote_ctx.request_history_kline(STOCK_CODE, start=START_DATE, end=END_DATE,
                                                                      max_count=1000,
                                                                      page_req_key=page_req_key)  # 请求翻页后的数据
            if ret == RET_OK:
                data_list.append(data)
            else:
                print('error:', data)
        data_pd = pd.DataFrame(data)
        data_pd.to_csv(STOCK_CODE + '.csv')
        print('All pages are finished!')
    quote_ctx.close()
