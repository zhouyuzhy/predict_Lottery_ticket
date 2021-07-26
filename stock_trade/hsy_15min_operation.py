from matplotlib.ticker import MultipleLocator

from stock_trade.constant import strategy_result_yes, max_loss_ratio
from stock_trade.model.asset import AssetSnapshot
from stock_trade.model.position import Position
from stock_trade.operation import IOperation
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt
import time
from copy import deepcopy

cache_15min_k = dict()
cache_day_k = dict()


def getCurDay15minK(curTime, history_data_15min):
    curDayDatas = history_data_15min.loc[history_data_15min['time_key'].str.contains(curTime[0:11])]
    curDateTime = datetime.fromisoformat(curTime)
    target_key = []
    for i in range(len(curDayDatas)):
        next_time_window = datetime.fromisoformat(curDayDatas.iloc[i]['time_key'])
        if '00:00:00' not in curTime and curDateTime < next_time_window:
            break
        target_key.append(next_time_window.strftime('%Y-%m-%d %H:%M:%S'))
    data_list = curDayDatas.loc[history_data_15min['time_key'].isin(target_key)]
    return data_list


def getCurDayDayK(curTime, history_data_day):
    cache_key = curTime[0:10]
    if cache_key in cache_day_k:
        return cache_day_k[cache_key]
    data_list = pd.DataFrame()
    curDateTime = datetime.fromisoformat(curTime)
    for i in range(len(history_data_day)):
        curDayData = history_data_day.iloc[i]
        if datetime.fromisoformat(curDayData['time_key']) <= curDateTime:
            data_list = data_list.append(curDayData, ignore_index=True)
        else:
            break
    cache_day_k[cache_key] = data_list
    return data_list


def market_close(recall_cur_data):
    if 'HK' in recall_cur_data['code']:
        return ' 16:00:00' in recall_cur_data['time_key']
    else:
        return ' 15:00:00' in recall_cur_data['time_key']


class Hsy15minOperation(IOperation):
    def __init__(self):
        pass

    def do_operation(self, asset, cur_data, history_data_15min, history_data_day):
        total_count = 0
        same_count = 0
        for i in range(len(history_data_day)):
            total_count+=1
            day_close_price = history_data_day.iloc[i]['close']
            day_open_price = history_data_day.iloc[i]['open']
            day_first_15min_high_price = getCurDay15minK(history_data_day.iloc[i]['time_key'], history_data_15min).iloc[0]['high']
            is_increase_for_close = (day_close_price - day_first_15min_high_price) >= 0
            is_increase_for_first_15min = (day_first_15min_high_price - day_open_price) >= 0
            if is_increase_for_close and is_increase_for_first_15min:
                same_count += 1
        print('总天数:', total_count, '相同天数：', same_count, '概率:', same_count * 1.0 / total_count)

