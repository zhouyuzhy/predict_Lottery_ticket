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
        # 持股变更记录
        self.operationsLogs = PositionOperationLog()


class AssetSnapshot:
    def __init__(self, time_key,  asset):
        self.time_key = time_key
        self.asset = copy.deepcopy(asset)


class PositionOperationLog:
    def __init__(self):
        self.operations = []

    def appendLog(self, position, op):
        self.operations.append((position, op))

