from futu import *
import pandas as pd
from datetime import datetime
from pyti.relative_strength_index import relative_strength_index as rsi


STOCK_CODE_MEITUAN = 'HK.03690'

STOCK_CODE_TENGXUN = 'HK.00700'

STOCK_CODE_BABA = 'HK.09988'

STOCK_CODE_MI = 'HK.01810'

STOCK_CODE_HENGSHENG = 'HK.800000'

STOCK_CODE_JD = 'HK.09618'

STOCK_CODE_WY = 'HK.09999'

STOCK_CODE_BYD = 'HK.01211'

STOCK_CODE_ZHONGXINGUOJI = 'HK.00981'

STOCK_CODE_HENGSHENG_KEJI = 'HK.800700'

STOCK_CODES = [STOCK_CODE_MEITUAN, STOCK_CODE_TENGXUN, STOCK_CODE_BABA, STOCK_CODE_MI, STOCK_CODE_HENGSHENG,
               STOCK_CODE_JD, STOCK_CODE_BYD, STOCK_CODE_ZHONGXINGUOJI, STOCK_CODE_HENGSHENG_KEJI]

START_DATE = '2017-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def crossesOver(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed over that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] <= stream2:
            return 0
        else:
            if stream1[len(stream1)-2] > stream2:
                return 0
            elif stream1[len(stream1)-2] < stream2:
                return 1
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x = x + 1
                if stream1[len(stream1)-x] < stream2:
                    return 1
                else:
                    return 0
    # Check if stream1 has crossed over stream2
    else:
        if stream1[len(stream1)-1] <= stream2[len(stream2)-1]:
            return 0
        else:
            if stream1[len(stream1)-2] > stream2[len(stream2)-2]:
                return 0
            elif stream1[len(stream1)-2] < stream2[len(stream2)-2]:
                return 1
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x = x + 1
                if stream1[len(stream1)-x] < stream2[len(stream2)-x]:
                    return 1
                else:
                    return 0


def crossesUnder(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed under that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] >= stream2:
            return 0
        else:
            if stream1[len(stream1)-2] < stream2:
                return 0
            elif stream1[len(stream1)-2] > stream2:
                return 1
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x = x + 1
                if stream1[len(stream1)-x] > stream2:
                    return 1
                else:
                    return 0
    # Check if stream1 has crossed under stream2
    else:
        if stream1[len(stream1)-1] >= stream2[len(stream2)-1]:
            return 0
        else:
            if stream1[len(stream1)-2] < stream2[len(stream2)-2]:
                return 0
            elif stream1[len(stream1)-2] > stream2[len(stream2)-2]:
                return 1
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x = x + 1
                if stream1[len(stream1)-x] > stream2[len(stream2)-x]:
                    return 1
                else:
                    return 0


RSI_KEYS = ['rsi6', 'rsi12', 'rsi24', 'crossover_6_12', 'crossover_6_24', 'crossover_12_24',
            'upper_crossover_rsi_6', 'upper_crossover_rsi_12', 'upper_crossover_rsi_24',
            'lower_crossover_rsi_6', 'lower_crossover_rsi_12', 'lower_crossover_rsi_24',
            'crossunder_6_12', 'crossunder_6_24', 'crossunder_12_24',
            'lower_crossunder_rsi_6', 'lower_crossunder_rsi_12', 'lower_crossunder_rsi_24',
            'upper_crossunder_rsi_6', 'upper_crossunder_rsi_12', 'upper_crossunder_rsi_24']

def set_rsi(data_pd):
    data_pd['rsi6'] = pd.Series(rsi(data_pd['close'], 6)).fillna(0).tolist()
    data_pd['rsi12'] = pd.Series(rsi(data_pd['close'], 12)).fillna(0).tolist()
    data_pd['rsi24'] = pd.Series(rsi(data_pd['close'], 24)).fillna(0).tolist()
    data_pd['crossover_6_12'] = [crossesOver(data_pd['rsi6'].values[:i+1], data_pd['rsi12'].values[:i+1]) for i in range(len(data_pd))]
    data_pd['crossover_6_24'] = [crossesOver(data_pd['rsi6'].values[:i+1], data_pd['rsi24'].values[:i+1]) for i in range(len(data_pd))]
    data_pd['crossover_12_24'] = [crossesOver(data_pd['rsi12'].values[:i+1], data_pd['rsi24'].values[:i+1]) for i in range(len(data_pd))]
    upper_rsi = 80
    lower_rsi = 30
    data_pd['upper_crossover_rsi_6'] = [crossesOver(data_pd['rsi6'].values[:i+1], upper_rsi) for i in range(len(data_pd))]
    data_pd['upper_crossover_rsi_12'] = [crossesOver(data_pd['rsi12'].values[:i+1], upper_rsi) for i in range(len(data_pd))]
    data_pd['upper_crossover_rsi_24'] = [crossesOver(data_pd['rsi24'].values[:i+1], upper_rsi) for i in range(len(data_pd))]
    data_pd['lower_crossover_rsi_6'] = [crossesOver(data_pd['rsi6'].values[:i+1], lower_rsi) for i in range(len(data_pd))]
    data_pd['lower_crossover_rsi_12'] = [crossesOver(data_pd['rsi12'].values[:i+1], lower_rsi) for i in range(len(data_pd))]
    data_pd['lower_crossover_rsi_24'] = [crossesOver(data_pd['rsi24'].values[:i+1], lower_rsi) for i in range(len(data_pd))]

    data_pd['crossunder_6_12'] = [crossesUnder(data_pd['rsi6'].values[:i+1], data_pd['rsi12'].values[:i+1]) for i in range(len(data_pd))]
    data_pd['crossunder_6_24'] = [crossesUnder(data_pd['rsi6'].values[:i+1], data_pd['rsi24'].values[:i+1]) for i in range(len(data_pd))]
    data_pd['crossunder_12_24'] = [crossesUnder(data_pd['rsi12'].values[:i+1], data_pd['rsi24'].values[:i+1]) for i in range(len(data_pd))]

    data_pd['lower_crossunder_rsi_6'] = [crossesUnder(data_pd['rsi6'].values[:i+1], lower_rsi) for i in range(len(data_pd))]
    data_pd['lower_crossunder_rsi_12'] = [crossesUnder(data_pd['rsi12'].values[:i+1], lower_rsi) for i in range(len(data_pd))]
    data_pd['lower_crossunder_rsi_24'] = [crossesUnder(data_pd['rsi24'].values[:i+1], lower_rsi) for i in range(len(data_pd))]
    data_pd['upper_crossunder_rsi_6'] = [crossesUnder(data_pd['rsi6'].values[:i+1], upper_rsi) for i in range(len(data_pd))]
    data_pd['upper_crossunder_rsi_12'] = [crossesUnder(data_pd['rsi12'].values[:i+1], upper_rsi) for i in range(len(data_pd))]
    data_pd['upper_crossunder_rsi_24'] = [crossesUnder(data_pd['rsi24'].values[:i+1], upper_rsi) for i in range(len(data_pd))]


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
        data_pd['incr'] = (data_pd['close']-data_pd['last_close']>0).astype(int)
        set_rsi(data_pd)
        data_pd.to_csv(STOCK_CODE + '.csv')
        print('All pages are finished!')
    quote_ctx.close()


if __name__ == '__main__':
    fetch_stock_datas()
