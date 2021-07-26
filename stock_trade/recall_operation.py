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
        if curDateTime < next_time_window:
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
            asset.operationsLogs.appendLog(position, 'sell', recall_cur_data['time_key'],
                                           earnings=(recall_cur_data['low'] - position.cost) * position.volume,
                                           sell_price=recall_cur_data['low'])
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
        asset.operationsLogs.appendLog(position, 'buy', recall_cur_data['time_key'])

    def recal_fund(self, recall_cur_data, asset):
        # 仅支持一只股票回溯，后续可扩展全部所需股票的每分钟数据用于重算资产
        fund_for_positions = 0
        if len(asset.positions) <= 0:
            return asset.money
        for position in asset.positions:
            if position.code != recall_cur_data['code']:
                raise Exception('不支持多只股票回溯')
            fund_for_positions += recall_cur_data['close'] * position.volume
        return fund_for_positions + asset.money

    def do_operation(self, asset, cur_data, history_data_15min, history_data_day):
        global cache_15min_k, cache_day_k
        asset = deepcopy(asset)
        cache_15min_k = dict()
        cache_day_k = dict()
        # 初始资产
        init_fund = asset.fund
        # 初始股票成本
        init_stock_cost = 0
        snapshots = []
        for i in range(len(cur_data)):
            recall_cur_data = cur_data.iloc[i]
            code = recall_cur_data['code']
            if init_stock_cost == 0:
                init_stock_cost = recall_cur_data['open']
            # 拿当前天当前时间之前的15min数据
            recall_history_data_15min = getCurDay15minK(recall_cur_data['time_key'], history_data_15min)
            # 拿当天之前的数据（含当天）
            recall_history_data_day = getCurDayDayK(recall_cur_data['time_key'], history_data_day)
            isPutSignal = self.strategy.is_put_signal(asset, recall_cur_data, recall_history_data_15min,
                                                      recall_history_data_day)
            if isPutSignal == strategy_result_yes:
                self.sell_out(asset, recall_cur_data)

            isCallSignal = self.strategy.is_call_signal(recall_cur_data, recall_history_data_15min,
                                                        recall_history_data_day)
            if isCallSignal == strategy_result_yes:
                self.buy_in(asset, recall_cur_data)

            # 每天下午4点收盘结算资产、记录当日收益率
            if market_close(recall_cur_data):
                fund = self.recal_fund(recall_cur_data, asset)
                asset.fund = fund
                asset.earnings = fund - init_fund
                asset.earnings_ratio = asset.earnings / init_fund
                stock_earnings_ratio = (recall_cur_data['close'] - init_stock_cost) / init_stock_cost
                snapshots.append(AssetSnapshot(recall_cur_data['time_key'], asset, stock_earnings_ratio))
                print('recall day finish', recall_cur_data['time_key'])
        for operation in asset.operationsLogs.operations:
            print(operation[2], operation[1], operation[0].cost, operation[3], operation[4])
        # 绘制收益对比图
        x = [snapshot.time_key[0:10] for snapshot in snapshots]
        y_fund_earnings_ratio = [snapshot.asset.earnings_ratio for snapshot in snapshots]
        y_stock_earnings_ratio = [snapshot.stock_earnings_ratio for snapshot in snapshots]
        fg = plt.figure()
        plt.title(code + ' Result Analysis ' + str(max_loss_ratio.max_loss_ratio))
        plt.plot(x, y_fund_earnings_ratio, color='green', label='fund earnings ratio')
        plt.plot(x, y_stock_earnings_ratio, color='skyblue', label='stock earnings ratio')
        plt.legend()
        plt.xlabel('time')
        plt.ylabel('earnings ratio')
        ax = fg.gca()
        x_major_locator = MultipleLocator(5)
        ax.xaxis.set_major_locator(x_major_locator)
        earnings_pd = pd.DataFrame()
        earnings_pd['x'] = x
        earnings_pd['y_fund_earnings_ratio'] = y_fund_earnings_ratio
        earnings_pd['y_stock_earnings_ratio'] = y_stock_earnings_ratio
        earnings_pd.to_csv('data/earnings_' + code + '.csv')
