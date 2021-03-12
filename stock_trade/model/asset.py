import copy


class Asset:
    def __init__(self, fund, positions, money, earnings):
        # 总资产
        self.fund = fund
        # 持股列表
        self.positions = positions
        # 持有资金
        self.money = money
        # 总收益
        self.earnings = earnings
        # 总收益率
        self.earnings_ratio = 0
        # 持股变更记录
        self.operationsLogs = PositionOperationLog()


class AssetSnapshot:
    def __init__(self, time_key,  asset, stock_earnings_ratio):
        self.time_key = time_key
        self.asset = copy.deepcopy(asset)
        self.stock_earnings_ratio = stock_earnings_ratio


class PositionOperationLog:
    def __init__(self):
        self.operations = []

    def appendLog(self, position, op, time_key, earnings=0, sell_price=0):
        self.operations.append((position, op, time_key, earnings, sell_price))

