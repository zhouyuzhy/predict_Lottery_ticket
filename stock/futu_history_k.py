from futu import *
import pandas as pd
from datetime import datetime
from stock.index.rsi.data_processor import set_rsi

STOCK_CODE_MEITUAN = 'HK.03690'

STOCK_CODE_TENGXUN = 'HK.00700'

STOCK_CODE_BABA = 'HK.09988'

STOCK_CODE_MI = 'HK.01810'

STOCK_CODE_HENGSHENG = 'HK.800000'

STOCK_CODE_JD = 'HK.09618'

STOCK_CODE_WY = 'HK.09999'

STOCK_CODE_BYD = 'HK.01211'

STOCK_CODE_JILI = 'HK.00175'

STOCK_CODE_ZGYD = 'HK.00941'

STOCK_CODE_ZHONGXINGUOJI = 'HK.00981'

STOCK_CODE_HENGSHENG_KEJI = 'HK.800700'

STOCK_CODES = [STOCK_CODE_MEITUAN, STOCK_CODE_TENGXUN, STOCK_CODE_BABA, STOCK_CODE_MI, STOCK_CODE_HENGSHENG,
               STOCK_CODE_JD, STOCK_CODE_BYD, STOCK_CODE_JILI, STOCK_CODE_ZGYD, STOCK_CODE_ZHONGXINGUOJI,
               STOCK_CODE_HENGSHENG_KEJI]

START_DATE = '2017-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def fetch_stock_datas():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_history_kl_quota(get_detail=True)  # 设置True代表需要返回详细的拉取历史K 线的记录
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
        raise Exception('unknown error')
    for STOCK_CODE in STOCK_CODES:
        data_list = pd.DataFrame()
        ret, data, page_req_key = quote_ctx.request_history_kline(STOCK_CODE, start=START_DATE, end=END_DATE,
                                                                  max_count=1000)  # 每页5个，请求第一页
        if ret == RET_OK:
            data_list = data
        else:
            print('error:', data)
            raise Exception('unknown error')
        while page_req_key is not None:  # 请求后面的所有结果
            print('*************************************')
            ret, data, page_req_key = quote_ctx.request_history_kline(STOCK_CODE, start=START_DATE, end=END_DATE,
                                                                      max_count=1000,
                                                                      page_req_key=page_req_key)  # 请求翻页后的数据
            if ret == RET_OK:
                data_list = data_list.append(data, ignore_index=True)
            else:
                print('error:', data)
                raise Exception('unknown error')
        data_pd = data_list
        data_pd['incr'] = (data_pd['close'] - data_pd['last_close'] > 0).astype(int)
        set_rsi(data_pd)
        data_pd.to_csv(STOCK_CODE + '.csv')
        print('All pages are finished!')
    quote_ctx.close()


if __name__ == '__main__':
    fetch_stock_datas()
