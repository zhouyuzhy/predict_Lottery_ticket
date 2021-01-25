import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import models, layers

dftrain_raw = None
dftest_raw = None


def load_data():
    global dftrain_raw, dftest_raw
    # dftrain_raw = pd.read_csv('https://raw.githubusercontent.com/lyhue1991/eat_tensorflow2_in_30_days/master/data/titanic/train.csv')
    dftrain_raw = pd.read_csv('./train1_1.csv')
    # dftest_raw = pd.read_csv('https://raw.githubusercontent.com/lyhue1991/eat_tensorflow2_in_30_days/master/data/titanic/test.csv')
    dftest_raw = pd.read_csv('./test1_1.csv')


def show_survived_data():
    ax = dftrain_raw['Survived'].value_counts().plot(kind='bar', figsize=(12, 8), fontsize=15, rot=0)
    ax.set_ylabel('counts', fontsize=15)
    ax.set_xlabel('Survived', fontsize=15)
    plt.show()


def show_age_data():
    ax = dftrain_raw['Age'].plot(kind='hist', bins=8)
    ax.set_ylabel('counts')
    ax.set_xlabel('Age')
    plt.show()


def show_relation_age_survived():
    ax = dftrain_raw.query('Survived==1')['Age'].plot(kind='density')
    dftrain_raw.query('Survived==0')['Age'].plot(kind='density')
    ax.legend(['Survived==1', 'Survived==0'])
    ax.set_ylabel('counts')
    ax.set_xlabel('Age')
    plt.show()


def preprocessing(dfdata):
    dfresult = pd.DataFrame()

    # Pclass
    dfPclass = pd.get_dummies(dfdata['Pclass'])
    dfPclass.columns = ['Pclass_' + str(x) for x in dfPclass.columns]
    dfresult = pd.concat([dfresult, dfPclass], axis=1)

    # Sex
    dfSex = pd.get_dummies(dfdata['Sex'])
    dfresult = pd.concat([dfresult, dfSex], axis=1)

    # Age
    dfresult['Age'] = dfdata['Age'].fillna(0)
    dfresult['Age_null'] = pd.isna(dfdata['Age']).astype('int32')

    # SibSp,Parch,Fare
    dfresult['SibSp'] = dfdata['SibSp']
    dfresult['Parch'] = dfdata['Parch']
    dfresult['Fare'] = dfdata['Fare']

    # Carbin
    dfresult['Cabin_null'] = pd.isna(dfdata['Cabin']).astype('int32')

    # Embarked
    dfEmbarked = pd.get_dummies(dfdata['Embarked'], dummy_na=True)
    dfEmbarked.columns = ['Embarked_' + str(x) for x in dfEmbarked.columns]
    dfresult = pd.concat([dfresult, dfEmbarked], axis=1)

    return (dfresult)


def plot_metric(history, metric):
    train_metrics = history.history[metric]
    val_metrics = history.history['val_' + metric]
    epochs = range(1, len(train_metrics) + 1)
    plt.plot(epochs, train_metrics, 'bo--')
    plt.plot(epochs, val_metrics, 'ro-')
    plt.title('Training and validation ' + metric)
    plt.xlabel("Epochs")
    plt.ylabel(metric)
    plt.legend(["train_" + metric, 'val_' + metric])
    plt.show()


if __name__ == '__main__':
    load_data()
    if False:
        show_survived_data()
    if False:
        show_age_data()
    if False:
        show_relation_age_survived()

    x_train = preprocessing(dftrain_raw)
    y_train = dftrain_raw['Survived'].values

    x_test = preprocessing(dftest_raw)
    y_test = dftest_raw['Survived'].values
    print("x_train.shape =", x_train.shape)
    print("x_test.shape =", x_test.shape)

    tf.keras.backend.clear_session()

    model = models.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(15,)))
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    print(model.summary())
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['AUC'])

    history = model.fit(x_train, y_train,
                        batch_size=64,
                        epochs=30,
                        validation_split=0.2  # 分割一部分训练数据用于验证
                        )
    plot_metric(history, "loss")
    plot_metric(history, "auc")
    auc_test = model.evaluate(x = x_test,y = y_test)
    print(auc_test)

    result = model.predict(x_test[0:10])
    print('predict', result)

    result = model.predict_classes(x_test[0:10])
    print('predict_classes', result)


