from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
import config
from config import CONVERT, X_ATTRIBUTES, Y_ATTRIBUTES
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from operator import itemgetter
from sklearn.linear_model import SGDClassifier
import get_train_data
import zsy.transfer_data


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values


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
    get_train_data.fetch_train_data()
    zsy.transfer_data.trans_data()
    # 处理原始数据,用前一期的X和本期的Y作为关联预测维度
    data, newest_X = process_data(CONVERT)
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    for ppl in [1, 2]:
        predict_red_results = []
        predict_blue_results = []
        for ball in config.BALL_ENUM:
            # for ball in [('红', 1)]:
            # 训练
            key = ball[0] + '_' + str(ball[1])
            if ppl == 1:
                pipeline = Pipeline([
                    ('selector', DataFrameSelector([config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key])),
                    # ('std_scaler', StandardScaler())
                ])
            elif ppl == 2:
                pipeline = Pipeline([
                    ('selector', DataFrameSelector([config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key])),
                    ('std_scaler', StandardScaler())
                ])
            prepared = pipeline.fit_transform(train_set)
            lin_reg = LinearRegression()
            lin_reg.fit(prepared, train_set[Y_ATTRIBUTES[key]].values)

            # sgd_clf = SGDClassifier(random_state=42)
            # sgd_clf.fit(prepared, train_set[Y_ATTRIBUTES[key]].values)

            # test预测
            predictions = lin_reg.predict(pipeline.fit_transform(test_set))
            # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
            # print(key, "predictions: ", predictions)
            targets = test_set[Y_ATTRIBUTES[key]]
            # print(key, "labels: ", list(targets))

            # test验证
            line_mse = mean_squared_error(targets, predictions)
            line_rmse = np.sqrt(line_mse)
            # print(line_rmse)

            # 组装下一期X并预测
            predictions = lin_reg.predict(pipeline.fit_transform(newest_X[[config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key]]))
            # predictions = sgd_clf.predict(pipeline.fit_transform(newest_X[[config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key]]))

            # print(key, ':', predictions)
            if '红' in key:
                predict_red_results.append((key, predictions[0]))
            if '蓝' in key:
                predict_blue_results.append((key, predictions[0]))
        print(sorted(predict_red_results, key=itemgetter(1), reverse=True)[0:6])
        print(sorted(predict_blue_results, key=itemgetter(1), reverse=True)[0])

