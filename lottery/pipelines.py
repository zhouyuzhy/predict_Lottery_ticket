from lottery.config import X_ATTRIBUTES, Y_ATTRIBUTES
import pandas as pd
from lottery import config, fetch_and_store
import lottery.transfer_data
import os

from lottery.line_regression_processor import processLRPrediction


def process_data(converted_data):
    result = {}
    newest_d_x = {}
    x_attributes = []
    y_attributes = []
    result[config.ATTRIBUTE_ISSUE] = converted_data[config.ATTRIBUTE_ISSUE].values[:-1]
    newest_d_x[config.ATTRIBUTE_ISSUE] = converted_data[config.ATTRIBUTE_ISSUE].values[0]
    for ball_item in config.BALL_ENUM:
        k = ball_item[0] + '_' + str(ball_item[1])
        result[Y_ATTRIBUTES[k]] = converted_data[Y_ATTRIBUTES[k]][:-1].values
        for column in X_ATTRIBUTES[k]:
            result[column] = converted_data[column][1:].values
            newest_d_x[column] = [converted_data[column][0]]
        x_attributes += X_ATTRIBUTES[k]
        y_attributes.append(Y_ATTRIBUTES[k])
    return pd.DataFrame(result, columns=[config.ATTRIBUTE_ISSUE] + y_attributes + x_attributes), pd.DataFrame(
        newest_d_x, columns=[config.ATTRIBUTE_ISSUE] + x_attributes)


if __name__ == '__main__':
    union_lotto_list = fetch_and_store.fetch()
    CONVERT = lottery.transfer_data.trans_data(union_lotto_list)
    # 处理原始数据,用前一期的X和本期的Y作为关联预测维度
    data, newest_X = process_data(CONVERT)
    processLRPrediction(data, newest_X)
