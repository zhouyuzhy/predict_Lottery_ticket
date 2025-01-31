# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 1:46 上午
# @Author  : niuzepeng
# @Site    : 
# @File    : config.py
import pandas as pd
import os.path

from lottery import CONVERT_ABSOLUTE_PATH
# from lottery import CONVERT_ABSOLUTE_PATH
URL = "https://datachart.500.com/ssq/history/"
path = "newinc/history.php?start={}&end="
# URL = "https://datachart.500.com/ssq/history/"
BOLL_NAME = [
    "红球号码_1",
    "红球号码_2",
    "红球号码_3",
    "红球号码_4",
    "红球号码_5",
    "红球号码_6",
    "蓝球"
]

BALL_ENUM = None

ATTRIBUTE_ISSUE = '期数'
X_ATTRIBUTES = None
Y_ATTRIBUTES = None
# 最近的数据数量
RECENT_COUNTS = [10, 30, 50, 100]

# 用于转换的数据
def init():
    global BALL_ENUM, X_ATTRIBUTES, Y_ATTRIBUTES, RECENT_COUNTS
    if BALL_ENUM is not None:
        return
    BALL_ENUM = []
    X_ATTRIBUTES = {}
    Y_ATTRIBUTES = {}
    for ball_type in ['红', '蓝']:
        for ball_num in range(1, 34):
            if ball_type == '蓝' and ball_num > 16:
                break
            BALL_ENUM.append((ball_type, ball_num))
            X_ATTRIBUTES[ball_type + '_' + str(ball_num)] = []
            for suffix in ['总次数_', '平均遗漏值_', '最大遗漏值_', '本次遗漏_', '上次遗漏_']:
                for recent_count in RECENT_COUNTS:
                    X_ATTRIBUTES[ball_type + '_' + str(ball_num)].append(
                        ball_type + '_' + str(ball_num) + '_' + suffix + str(recent_count))
            Y_ATTRIBUTES[ball_type + '_' + str(ball_num)] = ball_type + '_' + str(ball_num) + '_exist'


init()
if os.path.isfile(CONVERT_ABSOLUTE_PATH):
    CONVERT = pd.read_csv(CONVERT_ABSOLUTE_PATH)
else:
    CONVERT = None
