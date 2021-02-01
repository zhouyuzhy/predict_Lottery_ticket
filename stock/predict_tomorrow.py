import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from datetime import datetime as dt
import datetime
from sklearn.metrics import mean_squared_error
import numpy as np
import stock.data_processor as dp
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from stock import futu_history_k
import matplotlib.pyplot as plt
import os
import time

from stock.index.rsi.data_processor import RSI_KEYS


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        X_new['week_day'] = X_new.apply(lambda x: dt.strptime(x['time_key'], '%Y-%m-%d %H:%M:%S').weekday(),
                                        axis=1)
        return X_new[self.attribute_names + ['week_day']].values


TAGETs = ['high', 'low', 'open', 'close', 'incr']


def process_data(d1, TARGET):
    d = d1.copy()
    tomorrow_close = d[TARGET][:-1]
    l = [0]
    for tc in tomorrow_close:
        l.append(tc)
    d['tomorrow_' + TARGET] = l
    return d[1:]


def validate(targets, predictions):
    line_mse = mean_squared_error(targets, predictions)
    line_rmse = np.sqrt(line_mse)
    print(line_rmse)
    return line_rmse


def fix_incr_correct(last_day_prediction, time_key, today_real_incr, key_suffix=None):
    incr_key = 'incr'
    if key_suffix is not None:
        incr_key = incr_key + key_suffix
    last_day_prediction_incr = last_day_prediction.loc[last_day_prediction['date'].isin([time_key])][incr_key]
    if len(last_day_prediction_incr) == 0:
        return
    correct_key = 'correct'
    if key_suffix is not None:
        correct_key = correct_key + key_suffix
    if round(last_day_prediction_incr.values[0], 0) < 1:
        predict_incr = 0
    else:
        predict_incr = 1
    if len(today_real_incr.values) > 0:
        last_day_prediction.loc[last_day_prediction['date'].isin([time_key]), correct_key] = (
                    today_real_incr.values[0] == predict_incr)*1


def execute_predict():
    futu_history_k.fetch_stock_datas()
    for code in futu_history_k.STOCK_CODES:
        for lin_reg in [LinearRegression()]:
            print('----------', lin_reg, '-----------------')
            result = {}
            for TARGET in TAGETs:
                print('=========', TARGET, '============')
                data1 = pd.read_csv(code + '.csv')
                n = 5
                data = dp.concat_last_n_lines(data1, n)
                newest = data.head(1)
                data = process_data(data[1:-1 * n], TARGET)
                train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
                attrs = ['open', 'high', 'close', 'low', 'last_close', 'change_rate', 'incr'] + RSI_KEYS
                attrs = dp.concat_n_attrs(attrs, n)
                if isinstance(lin_reg, LinearRegression):
                    pipeline = Pipeline([
                        ('selector', DataFrameSelector(attrs)),
                    ])
                else:
                    pipeline = Pipeline([
                        ('selector', DataFrameSelector(attrs)),
                        ('std_scaler', StandardScaler())
                    ])
                prepared = pipeline.fit_transform(train_set)
                train_target = train_set['tomorrow_' + TARGET]
                lin_reg.fit(prepared, train_target)
                # test预测
                test_set_prepared = pipeline.fit_transform(test_set)
                predictions = lin_reg.predict(test_set_prepared)
                targets = test_set['tomorrow_' + TARGET]

                # test验证
                # if TARGET == 'incr':
                rmse = validate(targets, predictions)
                dp.val_score(lin_reg, prepared, train_target)
                sorted_attr_assoc = sorted(zip(lin_reg.coef_, attrs + ['week_day']), reverse=True)
                print('coef:', sorted_attr_assoc)
                # data.plot(kind='scatter', x=sorted_attr_assoc[0][1], y='tomorrow_'+TARGET, alpha=0.1)
                # plt.show()

                # 预测值
                predict = lin_reg.predict(pipeline.fit_transform(newest))
                print(code, '_', TARGET, predict)
                result[TARGET] = round(predict[0], 2)
                if TARGET == 'close':
                    result['rmse_' + TARGET] = round(result[TARGET] - round(rmse, 2) - newest['close'][0], 2)

            incr = None
            for key in result.keys():
                if key != 'close':
                    continue
                if result[key] > newest['close'][0]:
                    incr = 1
                elif result[key] < newest['close'][0]:
                    incr = 0
            result['current_close'] = newest['close'][0]
            result['incr_by_close_open'] = incr
            # 今天日期
            today = datetime.date.today()

            # 明天时间
            if today.weekday() >= 4:
                tomorrow = today + datetime.timedelta(days=7 - today.weekday())
            else:
                tomorrow = today + datetime.timedelta(days=1)
            result['date'] = tomorrow.strftime('%Y-%m-%d')
            result['correct'] = -2

            filePath = code + '_predict.csv'
            data_to_write = None
            if os.path.exists(filePath):
                data_to_write = pd.read_csv(filePath, index_col=0).append(result, ignore_index=True)
            else:
                data_to_write = pd.DataFrame(result, index=[0])
            today_real_incr = data1.loc[data1['time_key'].isin([today.strftime('%Y-%m-%d') + ' 00:00:00'])]['incr']
            key_suffix = '_by_close_open'
            fix_incr_correct(data_to_write, today.strftime('%Y-%m-%d'), today_real_incr)
            fix_incr_correct(data_to_write, today.strftime('%Y-%m-%d'), today_real_incr, key_suffix=key_suffix)
            data_to_write.drop_duplicates('date', keep='last', inplace=True)
            data_to_write = data_to_write.reindex(sorted(data_to_write.columns), axis=1)
            data_to_write.to_csv(filePath)


if __name__ == '__main__':
    need_while = True
    if need_while:
        while True:
            execute_predict()
            time_stamp = datetime.datetime.now()
            print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
            time.sleep(60)
    else:
        execute_predict()
