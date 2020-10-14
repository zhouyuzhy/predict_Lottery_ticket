# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 1:46 上午
# @Author  : niuzepeng
# @Site    : 
# @File    : config.py

URL = "https://datachart.500.com/ssq/history/"
path = "newinc/history.php?start={}&end="

BOLL_NAME = [
    "红球号码_1",
    "红球号码_2",
    "红球号码_3",
    "红球号码_4",
    "红球号码_5",
    "红球号码_6",
    "蓝球"
]

train_data_path = "data/data.csv"

BALL_ENUM = None


def init():
    global BALL_ENUM
    if BALL_ENUM is not None:
        return
    BALL_ENUM = []
    for ball_type in ['红', '蓝']:
        for ball_num in range(1, 34):
            if ball_type == '蓝' and ball_num > 16:
                break
            BALL_ENUM.append((ball_type, ball_num))


init()
