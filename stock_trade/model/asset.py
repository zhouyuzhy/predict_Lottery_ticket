
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
