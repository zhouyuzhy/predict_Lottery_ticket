from stock_trade.strategy import IStrategy


class YingStrategy(IStrategy):
    def is_call_signal(self, cur_data, history_data):
        pass

    def is_put_signal(self, cur_data, history_data):
        pass