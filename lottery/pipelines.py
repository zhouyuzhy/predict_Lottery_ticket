from lottery.config import X_ATTRIBUTES, Y_ATTRIBUTES
import pandas as pd
import numpy as np
from lottery import config, fetch_and_store
import lottery.transfer_data
import matplotlib.pyplot as plt
from lottery.line_regression_processor import processLRPrediction
from brokenaxes import brokenaxes


def process_data(converted_data, offset):
    history = {}
    newest_d_x = {}
    x_attributes = []
    y_attributes = []
    history[config.ATTRIBUTE_ISSUE] = converted_data[config.ATTRIBUTE_ISSUE].values[offset+1:]
    newest_d_x[config.ATTRIBUTE_ISSUE] = converted_data[config.ATTRIBUTE_ISSUE].values[offset]
    for ball_item in config.BALL_ENUM:
        k = ball_item[0] + '_' + str(ball_item[1])
        history[Y_ATTRIBUTES[k]] = converted_data[Y_ATTRIBUTES[k]][offset:-1].values
        for column in X_ATTRIBUTES[k]:
            history[column] = converted_data[column][offset+1:].values
            newest_d_x[column] = [converted_data[column][offset]]
        x_attributes += X_ATTRIBUTES[k]
        y_attributes.append(Y_ATTRIBUTES[k])
    return pd.DataFrame(history, columns=[config.ATTRIBUTE_ISSUE] + y_attributes + x_attributes), pd.DataFrame(
        newest_d_x, columns=[config.ATTRIBUTE_ISSUE] + x_attributes)


def visualize_total_10(data,ball,ball_num,cal_dim):
    key_dim = ball+'_'+str(ball_num)+'_'+cal_dim+'_10'
    key_exist = ball+'_'+str(ball_num)+'_exist'
    num = 300
    x = data[config.ATTRIBUTE_ISSUE].values[:num]
    y1 = data[key_exist].values[:num]
    y2 = data[key_dim].values[:num]
    xlims = []
    for i in range(19, 22):
        xlims.append((i * 1000 + 1, i * 1000 + 160))
    return x, y1, y2, xlims


def visualize_total_10_perc(data,ball,ball_num,cal_dim):
    key_dim = ball+'_'+str(ball_num)+'_'+cal_dim+'_10'
    key_exist = ball+'_'+str(ball_num)+'_exist'
    x = np.unique(data[key_dim])
    y = []
    for i in x:
        y.append(len(data.loc[(data[key_dim] == i) & (data[key_exist] == 1)])
                 / len(data.loc[data[key_dim] == i]))
    return x, y, y, [(0, np.max(data[key_dim])+1)]


def visualize(data):
    for m in [visualize_total_10, visualize_total_10_perc]:
        for ball_num in range(1,17):
            plt.figure()
            ball = '蓝'
            cal_dim = '总次数'
            x, y1, y2, xlims = m(data, ball, ball_num, cal_dim)

            bax = brokenaxes(xlims=xlims, hspace=.05)
            l1 = bax.plot(x, y1, 'r', label=ball+str(ball_num))
            l2 = bax.plot(x, y2, 'g', label=ball+str(ball_num))
            plt.title(ball+str(ball_num))
            bax.set_xlabel('row')
            bax.set_ylabel('column')
            bax.legend()
    plt.show()


if __name__ == '__main__':
    union_lotto_list = fetch_and_store.fetch()
    CONVERT = lottery.transfer_data.trans_data(union_lotto_list)
    # 处理原始数据,用前一期的X和本期的Y作为关联预测维度
    data, newest_X = process_data(CONVERT, 0)
    # visualize(data)
    processLRPrediction(data, newest_X)
    print('last one:'+str(newest_X[config.ATTRIBUTE_ISSUE]))
