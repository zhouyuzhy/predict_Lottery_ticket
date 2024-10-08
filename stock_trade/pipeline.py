from futu import *
from stock_trade.data_stream_15min_k import DataStream15minK
from stock_trade.data_stream_1min_k import DataStream1minK
from stock_trade.data_stream_day_k import DataStreamDayK
from stock_trade.constant import *
from stock_trade.hsy_15min_operation import Hsy15minOperation
from stock_trade.model.asset import Asset
from stock_trade.recall_operation import RecallOperation
from stock_trade.ying_strategy import YingStrategy
import matplotlib.pyplot as plt
import sys


if __name__ == '__main__':
    global max_loss_ratio
    code = STOCK_CODE_HSY
    if len(sys.argv) > 1:
        code = sys.argv[1]
        max_loss_ratio.max_loss_ratio = float(sys.argv[2])

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # 初始化资产信息
    asset = Asset(fund=50000, positions=[], money=50000, earnings=0)

    # 抓数据
    data_stream_1min_k = DataStream1minK(quote_ctx)
    data_stream_15min_k = DataStream15minK(quote_ctx)
    data_stream_day_k = DataStreamDayK(quote_ctx)
    codes = [code]
    start = '2020-01-01'
    end = '2021-03-11'
    plt.ion()
    for code in codes:
        data_1min_k_history = data_stream_1min_k.fetch_history(code, start, end)
        data_15min_k_history = data_stream_15min_k.fetch_history(code, start, end)
        data_day_k_history = data_stream_day_k.fetch_history(code, start, end)

        # 策略选择
        strategy = YingStrategy()

        # 操作链
        # operations = [RecallOperation(strategy)]
        operations = [Hsy15minOperation()]
        for operation in operations:
            operation.do_operation(asset, data_1min_k_history, data_15min_k_history, data_day_k_history)
    plt.ioff()
    plt.show()
    quote_ctx.close()