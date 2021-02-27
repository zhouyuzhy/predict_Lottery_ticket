from futu import *
from stock_trade.data_stream_15min_k import DataStream15minK
from stock_trade.data_stream_day_k import DataStreamDayK
from stock_trade.constant import *
from stock_trade.ying_strategy import YingStrategy

if __name__ == '__main__':
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    # 抓数据
    data_stream_15min_k = DataStream15minK(quote_ctx)
    data_stream_day_k = DataStreamDayK(quote_ctx)
    code = STOCK_CODE_BYD
    start = '2020-01-01'
    end = '2021-01-01'
    data_15min_k_history = data_stream_15min_k.fetch_history(code, start, end)
    data_day_k_history = data_stream_day_k.fetch_history(code, start, end)

    # 策略选择
    strategy = YingStrategy()

    # 操作链
    operations = []

    quote_ctx.close()