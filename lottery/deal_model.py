import pandas as pd


DATA = pd.read_csv("../data/convert.csv")
if not len(DATA):
    raise Exception("请执行 get_train_data.py 进行数据下载！")


if __name__ == '__main__':
    print(DATA)