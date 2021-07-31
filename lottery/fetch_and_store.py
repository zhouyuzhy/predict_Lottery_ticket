# -*- coding:utf-8 -*-
"""
Author: longjiang
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from lottery.config import *
from lottery.db import UnionLottoMapper
from lottery.db.model.UnionLotto import UnionLotto


def get_current_number():
    """ 获取最新一期数字
    :return: int
    """
    r = requests.get("{}{}".format(URL, "history.shtml"))
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    current_num = soup.find("div", class_="wrap_datachart").find("input", id="end")["value"]
    return int(current_num)


def spider(start, end):
    """ 爬取历史数据
    :param start 开始一期
    :param end 最近一期
    :return:
    """
    url = "{}{}{}".format(URL, path.format(start), end)
    r = requests.get(url=url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.find("tbody", attrs={"id": "tdata"}).find_all("tr")
    data = []
    for tr in trs:
        item = UnionLotto()
        item.periods= tr.find_all("td")[0].get_text().strip()
        item.red_ball_1 = tr.find_all("td")[1].get_text().strip()
        item.red_ball_2 = tr.find_all("td")[2].get_text().strip()
        item.red_ball_3 = tr.find_all("td")[3].get_text().strip()
        item.red_ball_4 = tr.find_all("td")[4].get_text().strip()
        item.red_ball_5 = tr.find_all("td")[5].get_text().strip()
        item.red_ball_6 = tr.find_all("td")[6].get_text().strip()
        item.blue_ball = tr.find_all("td")[7].get_text().strip()
        item.jackpot = tr.find_all("td")[9].get_text().strip().replace(',', '')
        item.first_prize_count = tr.find_all("td")[10].get_text().strip()
        item.first_prize_money = tr.find_all("td")[11].get_text().strip().replace(',', '')
        item.second_prize_count = tr.find_all("td")[12].get_text().strip()
        item.second_prize_money = tr.find_all("td")[13].get_text().strip().replace(',', '')
        item.buy_money = tr.find_all("td")[14].get_text().strip().replace(',', '')
        item.show_time = datetime.strptime(tr.find_all("td")[15].get_text().strip(),'%Y-%m-%d')
        data.append(item)

    return data


def fetch_and_store_data(start_period, end_period):
    need_fetch = False
    union_lotto_list_in_db = UnionLottoMapper.query_union_lotto_by_period(start_period, end_period)
    if len(union_lotto_list_in_db) <=0:
        need_fetch = True
    if len(union_lotto_list_in_db) > 0:
        if start_period >= union_lotto_list_in_db[0].periods \
                and end_period <= union_lotto_list_in_db[-1].periods:
            return union_lotto_list_in_db
        if start_period < union_lotto_list_in_db[0].periods:
            need_fetch = True
        if end_period > union_lotto_list_in_db[-1].periods:
            need_fetch = True
            start_period = union_lotto_list_in_db[-1].periods + 1
    union_lotto_list_spider = []
    if need_fetch:
        union_lotto_list_spider = spider(start_period, end_period)
        for union_lotto in union_lotto_list_spider:
            UnionLottoMapper.add_union_lotto(union_lotto)
    union_lotto_list_in_db.extend(union_lotto_list_spider)
    union_lotto_list_in_db.sort(key=lambda union_lotto: union_lotto.periods)
    return union_lotto_list_in_db


def fetch():
    return fetch_and_store_data(3001, get_current_number())
