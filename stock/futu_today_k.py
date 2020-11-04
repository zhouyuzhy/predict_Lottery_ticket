from futu import *
import pandas as pd
from datetime import datetime

STOCK_CODE = 'HK.800000'
START_DATE = '2017-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_sub, err_message = quote_ctx.subscribe([STOCK_CODE],
                                               [SubType.K_DAY, SubType.K_60M, SubType.K_30M, SubType.K_15M,
                                                SubType.K_5M, SubType.K_3M,
                                                SubType.K_1M], subscribe_push=False)
    # 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
    if ret_sub == RET_OK:  # 订阅成功
        for subType in [SubType.K_DAY, SubType.K_60M, SubType.K_30M, SubType.K_15M, SubType.K_5M, SubType.K_3M,
                        SubType.K_1M]:
            ret, data = quote_ctx.get_cur_kline(STOCK_CODE, 1000, subType, AuType.QFQ)
            if ret == RET_OK:
                pd.DataFrame(data).to_csv(STOCK_CODE + '_TODAY_' + subType + '.csv')
            else:
                print('error:', data)
    else:
        print('subscription failed', err_message)
    quote_ctx.close()
