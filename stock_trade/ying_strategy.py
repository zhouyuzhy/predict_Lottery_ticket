from stock_trade.constant import *
from stock_trade.recall_operation import getCurDay15minK
from stock_trade.strategy import IStrategy
from datetime import datetime

# 连续N天上盈线下移之后的突破才可买进
threshold_fall_down_days = 2
# 下盈线往下阈值
threshold_sell_low_line_ratio = 0.995
# 前高定义天数
threshold_days_last_high = 10


def break_through_high_win_line(cur_data, history_data_15min, history_data_day):
    # 上盈线连续向下，第一次突破上盈线，看多买牛
    if len(history_data_day) <= 2:
        return False
    fall_down_days = 0
    for i in range(len(history_data_day) - 2):
        next_day_data = history_data_day.iloc[-1 * (i + 2)]
        last_day_data = history_data_day.iloc[-1 * (i + 3)]
        if next_day_data['close'] * threshold_sell_low_line_ratio <= last_day_data['close'] \
                or next_day_data['high'] * threshold_sell_low_line_ratio <= last_day_data['high']:
            fall_down_days += 1
        else:
            if i + 4 > len(history_data_day):
                break
            last_last_day_data = history_data_day.iloc[-1 * (i + 4)]
            if next_day_data['close'] * threshold_sell_low_line_ratio <= last_last_day_data['close'] \
                    or next_day_data['high'] * threshold_sell_low_line_ratio <= last_last_day_data['high']:
                fall_down_days += 1
            else:
                break
    is_continue_fall_down = fall_down_days >= threshold_fall_down_days
    high_win_line = history_data_day.iloc[-2]['high']
    if is_continue_fall_down and cur_data['high'] >= high_win_line:
        return True
    return False


def fall_down_low_and_break_through(cur_data, history_data_15min, history_data_day):
    # 当日跌破前低后冲高过前低，看多只卖熊
    return False


def fall_down_low_win_line(cur_data, history_data_15min, history_data_day):
    # 当日跌破下盈线，看空卖牛
    if len(history_data_day) <= 1:
        return False
    cur_time = datetime.fromisoformat(cur_data['time_key'])
    is_before_15min = cur_time.hour == 9 and cur_time.minute < 45
    if is_before_15min:
        return False
    low_win_line = history_data_day.iloc[-2]['low']
    if cur_data['low'] <= low_win_line * threshold_sell_low_line_ratio:
        return True
    return False


def fall_dow_high_win_line(cur_data, history_data_15min, history_data_day):
    # 冲破（10日）前高回落到前高
    last_high = 0
    for i in range(threshold_days_last_high):
        if i + 2 > len(history_data_day):
            continue
        last_day_high = history_data_day.iloc[-1 * (i + 2)]['high']
        if last_day_high > last_high:
            last_high = last_day_high
    is_break_through = False
    if last_high == 0:
        return False
    for i in range(len(history_data_15min)):
        if history_data_15min.iloc[i]['high'] > last_high:
            is_break_through = True
            break
    if is_break_through and cur_data['low'] <= last_high:
        return True
    pass


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
        # if False and fall_dow_high_win_line(cur_data, history_data_15min, history_data_day):
        #     return strategy_result_yes
        return strategy_result_no
