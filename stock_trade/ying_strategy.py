from stock_trade.constant import *
from stock_trade.strategy import IStrategy


def break_through_dayk(cur_data, history_data_15min, history_data_day):
    # 上盈线连续向下，第一次突破上盈线
    if len(history_data_day) <= 1:
        return False
    fall_down_days = 0
    for i in range(len(history_data_day) - 1):
        next_day_data = history_data_day.iloc[-1 * (i+1)]
        last_day_data = history_data_day.iloc[-1 * (i+2)]
        if next_day_data['high'] <= last_day_data['high']:
            fall_down_days += 1
        else:
            break

    # 第一个15min逐渐突破上盈线

    # 第一个15min高开突破上盈线，第二个15min继续突破第一个15min
    pass


def fall_down_low_and_break_through(cur_data, history_data_15min, history_data_day):
    # 当日突破前高后回落至前高
    return False


class YingStrategy(IStrategy):
    def is_call_signal(self, cur_data, history_data_15min, history_data_day):
        if break_through_dayk(cur_data, history_data_15min, history_data_day):
            return strategy_result_yes
        if fall_down_low_and_break_through(cur_data, history_data_15min, history_data_day):
            return strategy_result_only_sell_put
        return strategy_result_no

    def is_put_signal(self, cur_data, history_data_15min, history_data_day):
        return strategy_result_no
