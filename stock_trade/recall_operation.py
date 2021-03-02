from stock_trade.operation import IOperation
from datetime import datetime,timedelta
import pandas as pd


def getCurDay15minK(curTime, history_data_15min):
    data_list = pd.DataFrame()
    curDayDatas = history_data_15min.loc[history_data_15min['time_key'].str.contains(curTime[0:11])]
    curDateTime = datetime.fromisoformat(curTime)
    for i in range(len(curDayDatas)):
        curDayData = curDayDatas.iloc[i]
        if datetime.fromisoformat(curDayData['time_key']) <= curDateTime + timedelta(minutes=15):
            data_list = data_list.append(curDayData, ignore_index=True)
        else:
            break
    return data_list


def getCurDayDayK(curTime, history_data_day):
    data_list = pd.DataFrame()
    curDateTime = datetime.fromisoformat(curTime)
    for i in range(len(history_data_day)):
        curDayData = history_data_day.iloc[i]
        if datetime.fromisoformat(curDayData['time_key']) <= curDateTime:
            data_list = data_list.append(curDayData, ignore_index=True)
        else:
            break
    return data_list


class RecallOperation(IOperation):
    def __init__(self, strategy):
        self.strategy = strategy

    def do_operation(self, asset, cur_data, history_data_15min, history_data_day):
        for i in range(len(cur_data)):
            recall_cur_data = cur_data.iloc[i]
            if '01-03' not in recall_cur_data['time_key']:
                continue
            # 拿当前天当前时间之前的15min数据
            recall_history_data_15min = getCurDay15minK(recall_cur_data['time_key'], history_data_15min)
            # 拿当天之前的数据（含当天）
            recall_history_data_day = getCurDayDayK(recall_cur_data['time_key'], history_data_day)
            isCallSignal = self.strategy.is_call_signal(recall_cur_data, recall_history_data_15min,
                                                        recall_history_data_day)
            isPutSignal = self.strategy.is_put_signal(recall_cur_data, recall_history_data_15min,
                                                      recall_history_data_day)
            print('curdata:', recall_cur_data)
            print('isCallSignal', isCallSignal)
            print('isPutSignal', isPutSignal)
            if i > 3:
                break

