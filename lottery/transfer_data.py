import pandas as pd
from config import *

DATA = pd.read_csv("../" + train_data_path)
if not len(DATA):
    raise Exception("请执行 get_train_data.py 进行数据下载！")

CONVERT = pd.read_csv("../data/convert.csv")


# 计算全量每一期次数、遗漏值等
# return [{"期数":20097,"红_1":{"exist":0, 遗漏值等...}}]
def construct_model(data_balls):
    results = CONVERT.to_dict('records') if len(CONVERT) > 0 else []
    for data_ball in data_balls:
        issue = data_ball['期数']
        if issue in CONVERT['期数'].values:
            continue
        result = {"期数": issue}
        for ball in BALL_ENUM:
            ball_key = ball[0] + '_' + str(ball[1])
            is_exist = cal_ball_exist(data_balls, issue, ball[1], ball[0])
            result[ball_key + '_exist'] = 1 if is_exist else 0
            for recent_count in RECENT_COUNTS:
                result[ball_key + '_总次数_' + str(recent_count)] = cal_total_count(data_balls, recent_count, ball[1],
                                                                                 ball[0], issue)
                missing_dict = cal_missing(data_balls, recent_count, ball[1], ball[0], issue)
                result[ball_key + '_平均遗漏值_' + str(recent_count)] = missing_dict['平均遗漏值']
                result[ball_key + '_最大遗漏值_' + str(recent_count)] = missing_dict['最大遗漏值']
                result[ball_key + '_本次遗漏_' + str(recent_count)] = missing_dict['本次遗漏']
                result[ball_key + '_上次遗漏_' + str(recent_count)] = missing_dict['上次遗漏']
        results.append(result)
    return results


def cal_ball_exist(data_balls, issue, ball_num, ball_type):
    for data_ball in data_balls:
        if data_ball['期数'] != issue:
            continue
        for exist_ball_num in data_ball[ball_type]:
            if exist_ball_num == ball_num:
                return True
        return False


# 最近recent_count期内出现总次数、平均遗漏值、最大遗漏值、上次遗漏
def cal_missing(data_balls, recent_count, ball_num, ball_type, issue=None):
    result = {}
    missing_count = cal_all_missing_count(data_balls, recent_count, ball_num, ball_type, issue)
    result['平均遗漏值'] = round(sum(missing_count) / len(missing_count), 2)
    result['最大遗漏值'] = max(missing_count)
    result['本次遗漏'] = missing_count[0] if len(missing_count) > 0 else 0
    result['上次遗漏'] = missing_count[1] if len(missing_count) > 1 else 0
    return result


# 计算指定期数内某个球所有遗漏值
# return: [10,5,3]
def cal_all_missing_count(data_balls, recent_count, ball_num, ball_type, issue=None):
    missing_counts = []
    missing_count = 0

    def reach_ball(b, t):
        nonlocal missing_count, missing_counts
        missing_counts.append(missing_count)
        missing_count = 0

    def missing_ball(b, t):
        nonlocal missing_count
        missing_count += 1

    def end_function(b, t):
        nonlocal missing_count, missing_counts
        missing_counts.append(missing_count)
        missing_count = 0

    for_loop_data_balls(data_balls, recent_count, ball_num, ball_type, issue, reach_ball, missing_ball, end_function)
    return missing_counts


# data_balls：[{"行":0,"期数":20098,"蓝":[1],"红":[1,2,3,4,5,6]}
# 计算最近指定期数内某个球出现的总次数
def cal_total_count(data_balls, recent_count, ball_num, ball_type, issue=None):
    having_count = 0

    def reach_ball(b, t):
        nonlocal having_count
        having_count += 1

    for_loop_data_balls(data_balls, recent_count, ball_num, ball_type, issue, reach_ball)
    return having_count


def for_loop_data_balls(data_balls, recent_count, ball_num, ball_type, issue=None,
                        reach_ball_function=None, missing_ball_function=None, end_function=None):
    count = 0
    reach_issue = False
    for data_ball in data_balls:
        if issue is not None and not reach_issue and data_ball['期数'] != issue:
            continue
        elif issue is not None and not reach_issue and data_ball['期数'] == issue:
            reach_issue = True
        missing = True
        if ball_type == '红':
            for ball in data_ball["红"]:
                if ball == ball_num and reach_ball_function is not None:
                    reach_ball_function(ball, ball_type)
                    missing = False
                    break
        elif ball_type == '蓝':
            for ball in data_ball["蓝"]:
                if ball == ball_num and reach_ball_function is not None:
                    reach_ball_function(ball, ball_type)
                    missing = False
        if missing and missing_ball_function is not None:
            missing_ball_function(ball_num, ball_type)
        count += 1
        if count >= recent_count:
            break
    if end_function is not None:
        end_function(ball_num, ball_type)


# [{"行":0,"期数":20098,"蓝":[1],"红":[1,2,3,4,5,6]}
def transfer_data_balls():
    data_balls = []
    for line in DATA.values:
        data_ball = dict()
        data_ball['行'] = line[0]
        data_ball['蓝'] = [line[8]]
        data_ball['期数'] = line[1]
        red_balls = []
        for i in range(2, 8):
            red_balls.append(line[+i])
        data_ball['红'] = red_balls
        data_balls.append(data_ball)
    return data_balls


def trans_data():
    data_ball_list = transfer_data_balls()

    model = construct_model(data_ball_list)
    # [{"期数":20097,"红_1":{"exist":0, 遗漏值等...}}]
    pd.DataFrame(model).sort_values('期数', axis=0, ascending=False).to_csv('../data/convert.csv', index=False)
