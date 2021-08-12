from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from lottery import config
from lottery.config import X_ATTRIBUTES, Y_ATTRIBUTES
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
from operator import itemgetter
from random import randint
import stock.data_processor as dp


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values


def processLRPrediction(data, newest_X):
    print('newest:', newest_X)
    lin_reg = LinearRegression()
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    red_balls = []
    blue_balls = []
    predict_red_results = []
    predict_blue_results = []
    for ball in config.BALL_ENUM:
        # 训练
        key = ball[0] + '_' + str(ball[1])
        if isinstance(lin_reg, LinearRegression):
            pipeline = Pipeline([
                ('selector', DataFrameSelector([config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key])),
            ])
        else:
            pipeline = Pipeline([
                ('selector', DataFrameSelector([config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key])),
                ('std_scaler', StandardScaler())
            ])
        prepared = pipeline.fit_transform(train_set)
        lin_reg.fit(prepared, train_set[Y_ATTRIBUTES[key]].values)

        # test预测
        predictions = lin_reg.predict(pipeline.fit_transform(test_set))
        # predictions = sgd_clf.predict(pipeline.fit_transform(test_set))
        # print(key, "predictions: ", predictions)
        targets = test_set[Y_ATTRIBUTES[key]]
        # print(key, "labels: ", list(targets))

        # test验证
        line_mse = mean_squared_error(targets, predictions)
        line_rmse = np.sqrt(line_mse)
        # print("line_rmse:", line_rmse)
        dp.val_score(lin_reg, prepared, train_set[Y_ATTRIBUTES[key]].values)

        # 组装下一期X并预测
        predictions = lin_reg.predict(pipeline.fit_transform(newest_X[[config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key]]))

        print(key, ':', predictions)
        if '红' in key:
            predict_red_results.append((key, predictions[0]))
        if '蓝' in key:
            predict_blue_results.append((key, predictions[0]))
    print(sorted(predict_red_results, key=itemgetter(1), reverse=True))
    print(sorted(predict_blue_results, key=itemgetter(1), reverse=True))
    for red_ball in sorted(predict_red_results, key=itemgetter(1), reverse=True)[0:12]:
        red_balls.append(int(red_ball[0].replace('红_', '')))
    for blue_ball in sorted(predict_blue_results, key=itemgetter(1), reverse=True)[0:3]:
        blue_balls.append(int(blue_ball[0].replace('蓝_', '')))
    red_balls = list(red_balls)
    blue_balls = list(blue_balls)
    print('red:', red_balls)
    print('blue:', blue_balls)
    result = red_balls[0:6]
    result = sorted(result)
    result.append('蓝' + str(blue_balls[0]))
    print('号：', result)
    n = 2
    for num in range(n):
        result = []
        for x in range(6):
            while True:
                random_ball = red_balls[randint(0, len(red_balls) - 1)]
                if random_ball not in result:
                    result.append(random_ball)
                    break
        result = sorted(result)
        result.append('蓝' + str(blue_balls[randint(0, len(blue_balls) - 1)]))
        print('号：', result)
