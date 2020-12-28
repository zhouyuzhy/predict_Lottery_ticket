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
from sklearn.ensemble import RandomForestRegressor


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy.loc[:, 'week_day'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').weekday(),
                                            axis=1)
        X_copy.loc[:, 'hour'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').hour, axis=1)
        X_copy.loc[:, 'minute'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').minute,
                                          axis=1)
        X_copy.loc[:, 'second'] = X.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').second,
                                          axis=1)

        return X_copy[self.attribute_names + ['week_day', 'hour', 'minute', 'second']].values


def process_data(d1, TARGET, next_n=5):
    d = d1.copy()
    for i in range(next_n):
        i = i + 1
        tomorrow_close = d[TARGET][:-1 * i]
        l = [0] * i
        for tc in tomorrow_close:
            l.append(tc)
        d['next_' + str(i) + '_' + TARGET] = l
    return d[next_n:]


# FILES = ['HK.800000_TODAY_K_1M.csv', 'HK.800000_TODAY_K_3M.csv', 'HK.800000_TODAY_K_5M.csv',
#                      'HK.800000_TODAY_K_15M.csv', 'HK.800000_TODAY_K_30M.csv', 'HK.800000_TODAY_K_60M.csv',
#                      'HK.800000_TODAY_K_DAY.csv']
FILES = ['HK.800000_TODAY_K_5M.csv']

if __name__ == '__main__':
    for lin_reg in [LinearRegression()]:
        print('------', lin_reg, '---------')
        for file in FILES:
            for TARGET in ['close', 'incr']:
                next_n = 5
                for i in range(next_n):
                    i = i+1
                    PREDICT_TARGET = 'next_'+str(i)+'_' + TARGET
                    data = pd.read_csv('today/' + file)
                    n = 5
                    data = dp.concat_last_n_lines(data, n)
                    data = process_data(data, TARGET, next_n)
                    newest = data.head(1)
                    data = data[1:-1 * n]
                    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
                    attrs = ['open', 'close', 'high', 'low', 'last_close', 'incr']
                    attrs = dp.concat_n_attrs(attrs, n)
                    pipeline = Pipeline([
                        ('selector', DataFrameSelector(attrs))
                    ])
                    prepared = pipeline.fit_transform(train_set)
                    lin_reg = LinearRegression()
                    lin_reg.fit(prepared, train_set[PREDICT_TARGET])
                    # test预测
                    predictions = lin_reg.predict(pipeline.fit_transform(test_set))
                    # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
                    # print(key, "predictions: ", predictions)
                    targets = test_set[PREDICT_TARGET]
                    # print(key, "labels: ", list(targets))

                    # test验证
                    line_mse = mean_squared_error(targets, predictions)
                    line_rmse = np.sqrt(line_mse)
                    dp.val_score(lin_reg, prepared, train_set[PREDICT_TARGET])
                    print(file, PREDICT_TARGET, '_RMSE:', line_rmse)
                    sorted_attr_assoc = sorted(zip(lin_reg.coef_, attrs + ['week_day', 'hour', 'minute', 'second']), reverse=True)

                    print(file, PREDICT_TARGET, 'coef:', sorted_attr_assoc)
                    # predict
                    predict = lin_reg.predict(pipeline.fit_transform(newest))
                    print(file, PREDICT_TARGET, '_predict:', predict)
                    print('----------------')
