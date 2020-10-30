import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import mean_squared_error
import numpy as np


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['week_day'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').weekday(), axis=1)
        return X[self.attribute_names + ['week_day']].values


def process_data(d):
    tomorrow_close = d['close'][1:]
    l = []
    for tc in tomorrow_close:
        l.append(tc)
    l.append(0)
    d['tomorrow_close'] = l
    return d[0:-1]


if __name__ == '__main__':
    data = pd.read_csv('HK800000.csv')
    newest = data.tail(1)
    data = process_data(data[0:-1])
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ('selector', DataFrameSelector(['open', 'high', 'close', 'change_rate', 'low', 'change_rate', 'last_close'])),
        # ('std_scaler', StandardScaler())
    ])
    prepared = pipeline.fit_transform(train_set)
    lin_reg = LinearRegression()
    lin_reg.fit(prepared, train_set['tomorrow_close'])
    # test预测
    predictions = lin_reg.predict(pipeline.fit_transform(test_set))
    # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
    # print(key, "predictions: ", predictions)
    targets = test_set['tomorrow_close']
    # print(key, "labels: ", list(targets))

    # test验证
    line_mse = mean_squared_error(targets, predictions)
    line_rmse = np.sqrt(line_mse)
    print(line_rmse)

    # predict
    # newest = pd.DataFrame(
    #     [{'time_key': '2020-10-29 00:00:00', 'close': 24586.60, 'change_rate':-0.49, 'open': 24290.01, 'high': 24678.90, 'low': 24258.56,
    #       'last_close': 24708.80}])
    predict = lin_reg.predict(pipeline.fit_transform(newest))
    print(predict)
