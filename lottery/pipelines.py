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
import lottery.transfer_data
import os
from random import randint
import stock.data_processor as dp
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVR
from keras import models
from keras import layers
import matplotlib.pyplot as plt


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


def line_predict():
    lin_reg = LinearRegression()
    # 处理原始数据,用前一期的X和本期的Y作为关联预测维度
    data, newest_X = process_data(CONVERT)
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    red_balls = set()
    blue_balls = set()
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
        print(key, "predictions: ", predictions)
        targets = test_set[Y_ATTRIBUTES[key]]
        # print(key, "labels: ", list(targets))

        # test验证
        line_mse = mean_squared_error(targets, predictions)
        line_rmse = np.sqrt(line_mse)
        print("line_rmse:", line_rmse)
        dp.val_score(lin_reg, prepared, train_set[Y_ATTRIBUTES[key]].values)

        # 组装下一期X并预测
        predictions = lin_reg.predict(pipeline.fit_transform(newest_X[[config.ATTRIBUTE_ISSUE] + X_ATTRIBUTES[key]]))

        print(key, ':', predictions)
        if '红' in key:
            predict_red_results.append((key, predictions[0]))
        if '蓝' in key:
            predict_blue_results.append((key, predictions[0]))
    print(sorted(predict_red_results, key=itemgetter(1), reverse=True)[0:12])
    print(sorted(predict_blue_results, key=itemgetter(1), reverse=True)[0:3])
    for red_ball in sorted(predict_red_results, key=itemgetter(1), reverse=True)[0:12]:
        red_balls.add(int(red_ball[0].replace('红_', '')))
    for blue_ball in sorted(predict_blue_results, key=itemgetter(1), reverse=True)[0:3]:
        blue_balls.add(int(blue_ball[0].replace('蓝_', '')))
    red_balls = sorted(list(red_balls))
    blue_balls = sorted(list(blue_balls))
    print('red:', red_balls)
    print('blue:', blue_balls)
    return red_balls, blue_balls


def network_predict():
    data, newest_X = process_data(CONVERT)
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    x_attributes = []
    for attr in X_ATTRIBUTES.values():
        x_attributes.extend(attr)
    red_x_attributes = []
    blue_x_attributes = []

    for attr in x_attributes:
        if '红' in attr:
            red_x_attributes.append(attr)
        if '蓝' in attr:
            blue_x_attributes.append(attr)
    red_y_attributes = []
    blue_y_attributes = []

    for attr in Y_ATTRIBUTES.values():
        if '红' in attr:
            red_y_attributes.append(attr)
        if '蓝' in attr:
            blue_y_attributes.append(attr)
    partial_x_train = train_set[[config.ATTRIBUTE_ISSUE] + blue_x_attributes]
    partial_y_train = train_set[blue_y_attributes]
    x_val = test_set[[config.ATTRIBUTE_ISSUE] + blue_x_attributes]
    y_val = test_set[blue_y_attributes]
    red_balls = set()
    blue_balls = set()
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(321,)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(16, activation='softmax'))
    model.compile(optimizer='rmsprop',
            loss='categorical_crossentropy',
            metrics=['accuracy'])
    history = model.fit(partial_x_train,
        partial_y_train,
        epochs=3,
        batch_size=128,
        validation_data=(x_val, y_val))
    predictions = model.predict(newest_X[[config.ATTRIBUTE_ISSUE] + blue_x_attributes])
    print(predictions.shape)
    print(np.sum(predictions[0]))
    print(np.argmax(predictions[0]))
    print(predictions[0][np.argmax(predictions[0])])
    print(predictions)

    # loss = history.history['loss']
    # val_loss = history.history['val_loss']
    # epochs = range(1, len(loss) + 1)
    # plt.plot(epochs, loss, 'bo', label='Training loss')
    # plt.plot(epochs, val_loss, 'b', label='Validation loss')
    # plt.title('Training and validation loss')
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.legend()
    # plt.show()
    #
    # acc = history.history['accuracy']
    # val_acc = history.history['val_accuracy']
    # plt.plot(epochs, acc, 'bo', label='Training acc')
    # plt.plot(epochs, val_acc, 'b', label='Validation acc')
    # plt.title('Training and validation accuracy')
    # plt.xlabel('Epochs')
    # plt.ylabel('Accuracy')
    # plt.legend()
    # plt.show()


if __name__ == '__main__':
    get_train_data.fetch_train_data()
    lottery.transfer_data.trans_data()
    network_predict()

    # if os.path.isfile('../data/convert.csv'):
    #     CONVERT = pd.read_csv("../data/convert.csv")
    # else:
    #     CONVERT = None
    # red_balls, blue_balls = line_predict()
    # n = 3
    # for num in range(n):
    #     result = []
    #     for x in range(6):
    #         while True:
    #             random_ball = red_balls[randint(0, len(red_balls) - 1)]
    #             if random_ball not in result:
    #                 result.append(random_ball)
    #                 break
    #     result = sorted(result)
    #     result.append('蓝'+str(blue_balls[randint(0, len(blue_balls) - 1)]))
    #     print('号：', result)
