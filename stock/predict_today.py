import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import mean_squared_error
import numpy as np
import stock.data_processor as dp


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy.loc[:, 'week_day'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').weekday(), axis=1)
        X_copy.loc[:, 'hour'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').hour, axis=1)
        X_copy.loc[:, 'minute'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').minute, axis=1)
        X_copy.loc[:, 'second'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').second, axis=1)

        return X_copy[self.attribute_names + ['week_day', 'hour', 'minute', 'second']].values


if __name__ == '__main__':
    for file in ['HK.800000_TODAY_K_1M.csv', 'HK.800000_TODAY_K_3M.csv', 'HK.800000_TODAY_K_5M.csv',
                 'HK.800000_TODAY_K_15M.csv', 'HK.800000_TODAY_K_30M.csv', 'HK.800000_TODAY_K_60M.csv',
                 'HK.800000_TODAY_K_DAY.csv']:
        data = pd.read_csv(file)
        n = 5
        data = dp.concat_last_n_lines(data, n)
        newest = data.head(1)
        data = data[1:-1*n]
        train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
        attrs = ['open', 'high', 'low', 'last_close']
        attrs = dp.concat_n_attrs(attrs, n)
        pipeline = Pipeline([
            ('selector', DataFrameSelector(attrs)),
            # ('std_scaler', StandardScaler())
        ])
        prepared = pipeline.fit_transform(train_set)
        lin_reg = LinearRegression()
        lin_reg.fit(prepared, train_set['close'])
        # test预测
        predictions = lin_reg.predict(pipeline.fit_transform(test_set))
        # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
        # print(key, "predictions: ", predictions)
        targets = test_set['close']
        # print(key, "labels: ", list(targets))

        # test验证
        line_mse = mean_squared_error(targets, predictions)
        line_rmse = np.sqrt(line_mse)
        print(file, ':', line_rmse)

        # predict
        # data = pd.read_csv('HK.800000_TODAY_DAY_K.csv')
        # newest = pd.DataFrame([{'time_key': '2020-10-29 00:00:00', 'open': 24290.01, 'high': 24678.90, 'low': 24258.56,
        #                         'last_close': 24708.80}])
        # newest = data.tail(1)
        predict = lin_reg.predict(pipeline.fit_transform(newest))
        print(file, ':', predict)
