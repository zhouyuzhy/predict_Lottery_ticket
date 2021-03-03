from stock_trade.constant import *
from stock_trade.strategy import IStrategy

# 连续N天上盈线下移之后的突破才可买进
threshold_fall_down_days = 1


def break_through_high_win_line(cur_data, history_data_15min, history_data_day):
    # 上盈线连续向下，第一次突破上盈线，看多买牛
    if len(history_data_day) <= 2:
        return False
    fall_down_days = 0
    for i in range(len(history_data_day) - 2):
        next_day_data = history_data_day.iloc[-1 * (i+2)]
        last_day_data = history_data_day.iloc[-1 * (i+3)]
        if next_day_data['high'] <= last_day_data['high']:
            fall_down_days += 1
        else:
            break
    if fall_down_days < threshold_fall_down_days:
        return False
    high_win_line = history_data_day.iloc[-2]['high']
    if cur_data['high'] >= high_win_line:
        return True
    return False


def fall_down_low_and_break_through(cur_data, history_data_15min, history_data_day):
    # 当日跌破前低后冲高过前低，看多只卖熊
    return False


def fall_down_low_win_line(cur_data, history_data_15min, history_data_day):
    # 当日跌破下盈线，看空卖牛
    if len(history_data_day) <= 1:
        return False
    low_win_line = history_data_day.iloc[-1]['low']
    if cur_data['low'] <= low_win_line:
        return True
    return False


class YingStrategy(IStrategy):
    def is_call_signal(self, cur_data, history_data_15min, history_data_day):
        if break_through_high_win_line(cur_data, history_data_15min, history_data_day):
            return strategy_result_yes
        if fall_down_low_and_break_through(cur_data, history_data_15min, history_data_day):
            return strategy_result_only_sell_put
        return strategy_result_no

    def is_put_signal(self, cur_data, history_data_15min, history_data_day):
        if fall_down_low_win_line(cur_data, history_data_15min, history_data_day):
            return strategy_result_yes
        return strategy_result_no
