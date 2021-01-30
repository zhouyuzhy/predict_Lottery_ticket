from stock.index.utils import crossesOver, crossesUnder
import pandas as pd
from pyti.relative_strength_index import relative_strength_index as rsi


RSI_KEYS = ['rsi6', 'rsi12', 'rsi24', 'crossover_6_12', 'crossover_6_24', 'crossover_12_24',
            'upper_crossover_rsi_6', 'upper_crossover_rsi_12', 'upper_crossover_rsi_24',
            'lower_crossover_rsi_6', 'lower_crossover_rsi_12', 'lower_crossover_rsi_24',
            'crossunder_6_12', 'crossunder_6_24', 'crossunder_12_24',
            'lower_crossunder_rsi_6', 'lower_crossunder_rsi_12', 'lower_crossunder_rsi_24',
            'upper_crossunder_rsi_6', 'upper_crossunder_rsi_12', 'upper_crossunder_rsi_24']


def rsi_cross_over_on_low(stream1, stream2):
    if stream1[len(stream1) - 2] >= 50 or stream2[len(stream2) - 2] >= 50:
        return 0
    return crossesOver(stream1, stream2)


def rsi_cross_under_on_high(stream1, stream2):
    if stream1[len(stream1) - 2] <= 50 or stream2[len(stream2) - 2] <= 50:
        return 0
    return crossesUnder(stream1, stream2)


def set_rsi(data_pd):
    upper_rsi = 80
    lower_rsi = 20

    data_pd['rsi6'] = pd.Series(rsi(data_pd['close'], 6)).fillna(0).tolist()
    data_pd['rsi12'] = pd.Series(rsi(data_pd['close'], 12)).fillna(0).tolist()
    data_pd['rsi24'] = pd.Series(rsi(data_pd['close'], 24)).fillna(0).tolist()

    # 1、超买超卖点位
    high_low_point(data_pd, lower_rsi, upper_rsi)

    # 2、金叉死叉
    cross_point(data_pd)

    # 3、双顶双底形态

    # 4、顶背离底背离形态


def high_low_point(data_pd, lower_rsi, upper_rsi):
    # RSI超买
    data_pd['upper_crossover_rsi_6'] = [crossesOver(data_pd['rsi6'].values[:i + 1], upper_rsi) for i in
                                        range(len(data_pd))]
    data_pd['upper_crossover_rsi_12'] = [crossesOver(data_pd['rsi12'].values[:i + 1], upper_rsi) for i in
                                         range(len(data_pd))]
    data_pd['upper_crossover_rsi_24'] = [crossesOver(data_pd['rsi24'].values[:i + 1], upper_rsi) for i in
                                         range(len(data_pd))]
    # RSI低位突破
    data_pd['lower_crossover_rsi_6'] = [crossesOver(data_pd['rsi6'].values[:i + 1], lower_rsi) for i in
                                        range(len(data_pd))]
    data_pd['lower_crossover_rsi_12'] = [crossesOver(data_pd['rsi12'].values[:i + 1], lower_rsi) for i in
                                         range(len(data_pd))]
    data_pd['lower_crossover_rsi_24'] = [crossesOver(data_pd['rsi24'].values[:i + 1], lower_rsi) for i in
                                         range(len(data_pd))]
    # RSI超卖
    data_pd['lower_crossunder_rsi_6'] = [crossesUnder(data_pd['rsi6'].values[:i + 1], lower_rsi) for i in
                                         range(len(data_pd))]
    data_pd['lower_crossunder_rsi_12'] = [crossesUnder(data_pd['rsi12'].values[:i + 1], lower_rsi) for i in
                                          range(len(data_pd))]
    data_pd['lower_crossunder_rsi_24'] = [crossesUnder(data_pd['rsi24'].values[:i + 1], lower_rsi) for i in
                                          range(len(data_pd))]
    # RSI高位回落
    data_pd['upper_crossunder_rsi_6'] = [crossesUnder(data_pd['rsi6'].values[:i + 1], upper_rsi) for i in
                                         range(len(data_pd))]
    data_pd['upper_crossunder_rsi_12'] = [crossesUnder(data_pd['rsi12'].values[:i + 1], upper_rsi) for i in
                                          range(len(data_pd))]
    data_pd['upper_crossunder_rsi_24'] = [crossesUnder(data_pd['rsi24'].values[:i + 1], upper_rsi) for i in
                                          range(len(data_pd))]


def cross_point(data_pd):
    # RSI低位金叉
    data_pd['crossover_6_12'] = [rsi_cross_over_on_low(data_pd['rsi6'].values[:i + 1], data_pd['rsi12'].values[:i + 1])
                                 for i in
                                 range(len(data_pd))]
    data_pd['crossover_6_24'] = [rsi_cross_over_on_low(data_pd['rsi6'].values[:i + 1], data_pd['rsi24'].values[:i + 1])
                                 for i in
                                 range(len(data_pd))]
    data_pd['crossover_12_24'] = [
        rsi_cross_over_on_low(data_pd['rsi12'].values[:i + 1], data_pd['rsi24'].values[:i + 1]) for i in
        range(len(data_pd))]
    # RSI高位死叉
    data_pd['crossunder_6_12'] = [
        rsi_cross_under_on_high(data_pd['rsi6'].values[:i + 1], data_pd['rsi12'].values[:i + 1]) for i in
        range(len(data_pd))]
    data_pd['crossunder_6_24'] = [
        rsi_cross_under_on_high(data_pd['rsi6'].values[:i + 1], data_pd['rsi24'].values[:i + 1]) for i in
        range(len(data_pd))]
    data_pd['crossunder_12_24'] = [
        rsi_cross_under_on_high(data_pd['rsi12'].values[:i + 1], data_pd['rsi24'].values[:i + 1]) for i
        in range(len(data_pd))]

