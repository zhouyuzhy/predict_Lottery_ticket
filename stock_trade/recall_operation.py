from stock_trade.model.position import Position
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

    def sell_out(self, asset, recall_cur_data):
        positions = asset.positions
        if len(positions) == 0:
            return
        to_clear_positions = []
        for position in positions:
            if position.code != recall_cur_data['code']:
                continue
            # 待减仓数据
            to_clear_positions.append(position)
            # 加钱
            asset.money = asset.money + recall_cur_data['low'] * position.volume
            # 记log
            asset.operationsLogs.appendLog(position, 'sell')
        # 平仓
        for position in to_clear_positions:
            positions.remove(position)

    def buy_in(self, asset, recall_cur_data):
        buy_in_price = recall_cur_data['high']
        position_volume = int(asset.money / (buy_in_price * 100)) * 100
        if position_volume < 100:
            return
        # 加持仓
        position = Position(recall_cur_data['code'], buy_in_price, position_volume, 0)
        asset.positions.append(position)
        # 减钱
        asset.money = asset.money - buy_in_price * position_volume
        # 记log
        asset.operationsLogs.appendLog(position, 'buy')

    def do_operation(self, asset, cur_data, history_data_15min, history_data_day):
        # 初始资产
        init_fund = asset.fund
        snapshots = []
        for i in range(len(cur_data)):
            recall_cur_data = cur_data.iloc[i]
            # 拿当前天当前时间之前的15min数据
            recall_history_data_15min = getCurDay15minK(recall_cur_data['time_key'], history_data_15min)
            # 拿当天之前的数据（含当天）
            recall_history_data_day = getCurDayDayK(recall_cur_data['time_key'], history_data_day)
            isPutSignal = self.strategy.is_put_signal(recall_cur_data, recall_history_data_15min,
                                                      recall_history_data_day)
            if isPutSignal:
                self.sell_out(asset, recall_cur_data)

            isCallSignal = self.strategy.is_call_signal(recall_cur_data, recall_history_data_15min,
                                                        recall_history_data_day)
            if isCallSignal:
                self.buy_in(asset, recall_cur_data)

            # 每天下午4点收盘结算资产、记录当日收益率
            if ' 16:00:00' in recall_cur_data['time_key']:
                pass






