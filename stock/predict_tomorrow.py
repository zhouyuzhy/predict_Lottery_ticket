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
from sklearn.model_selection import cross_val_score



class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        X_new['week_day'] = X_new.apply(lambda x: datetime.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').weekday(), axis=1)
        return X_new[self.attribute_names + ['week_day']].values


TAGETs = ['high', 'low', 'open', 'close']


def process_data(d1, TARGET):
    d = d1.copy()
    tomorrow_close = d[TARGET][1:]
    l = []
    for tc in tomorrow_close:
        l.append(tc)
    l.append(0)
    d['tomorrow_'+TARGET] = l
    return d[0:-1]


def validate(targets, predictions):
    line_mse = mean_squared_error(targets, predictions)
    line_rmse = np.sqrt(line_mse)
    print(line_rmse)


if __name__ == '__main__':
    for lin_reg in [RandomForestRegressor()]:
        print('----------', lin_reg, '-----------------')
        for TARGET in TAGETs:
            data = pd.read_csv('HK800000.csv')
            n = 5
            data = dp.concat_last_n_lines(data, n)
            newest = data.head(1)
            data = process_data(data[1:-1*n], TARGET)
            train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
            attrs = ['open', 'high', 'close', 'low', 'last_close']
            dp.concat_n_attrs(attrs, n)
            pipeline = Pipeline([
                ('selector', DataFrameSelector(attrs)),
                #('std_scaler', StandardScaler())
            ])
            prepared = pipeline.fit_transform(train_set)
            lin_reg.fit(prepared, train_set['tomorrow_'+TARGET])
            # test预测
            predictions = lin_reg.predict(pipeline.fit_transform(test_set))
            # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
            # print(key, "predictions: ", predictions)
            targets = test_set['tomorrow_'+TARGET]
            # print(key, "labels: ", list(targets))

            # test验证
            validate(targets, predictions)
            dp.val_score(lin_reg, prepared, train_set['tomorrow_'+TARGET])

            # predict
            # newest = pd.DataFrame(
            #     [{'time_key': '2020-10-29 00:00:00', 'close': 24586.60, 'change_rate':-0.49, 'open': 24290.01, 'high': 24678.90, 'low': 24258.56,
            #       'last_close': 24708.80}])
            predict = lin_reg.predict(pipeline.fit_transform(newest))
            print(TARGET, predict)
