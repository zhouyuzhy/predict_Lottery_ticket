from futu import *

from stock_trade.data_stream import BaseDataStream


class DataStream1minK(BaseDataStream):
    def __init__(self, quote_ctx):
        self.quote_ctx = None
        self.ktype = None
        super().__init__(quote_ctx, KLType.K_1M)

    def fetch_history(self, code, start, end):
        return super().fetch_history(code, start, end, True)

    def fetch_cur(self, code, num):
        return super().fetch_cur(code, num)

    def subscribe_k_handle(self, code, handler):
        pass
