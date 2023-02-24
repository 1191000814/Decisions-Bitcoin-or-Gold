"""
三种因素: rsi, 长期预测, 短期预测
"""

import numpy as np
import pandas as pd

from RSI import Rsi
from MACD import Macd
from icecream import ic

SHORT_FORCAST = 15 # 用前多少天评价灰色短期预测

def day_short_grade(day, gray_list):
    """
    预测一天的灰色评分
    """
    assert day >= SHORT_FORCAST
    refer_days = gray_list[day - SHORT_FORCAST : day]
    refer_days = sorted(refer_days) # 排序, 看改天位于前15天的哪个分位
    n = 0
    for i in range(SHORT_FORCAST):
        if gray_list[day] > refer_days[i]:
            n += 1
        else:
            break
    fractile = n / SHORT_FORCAST
    if fractile > 0.7:
        return 1
    elif fractile > 0.3:
        return 0.5
    else:
        return 0


def get_gray_grade(gray_list):
    """
    预测所有天的灰色评分
    """
    days = len(gray_list)
    gray_grade = np.zeros((days, ))
    for day in range(SHORT_FORCAST, days):
        gray_grade[day] = day_short_grade(day, gray_list)
    return gray_grade


def get_rsi_grade(rsi_list):
    """
    rsi指标的评分
    """
    days = len(rsi_list)
    rsi_grade = np.zeros((days,))
    for day in range(days):
        if rsi_list[day] > 0.8:
            rsi_grade[day] = 0.2
        elif rsi_list[day] > 0.5:
            rsi_grade[day] = 1
        elif rsi_list[day] > 0.2:
            rsi_grade[day] = 0.2
        else:
            rsi_grade[day] = 0.8
    return rsi_grade


def get_overall_grade(lstm_grade, gray_grade, rsi_grade):
    """
    三种指标的综合评分
    """
    return (lstm_grade + rsi_grade + gray_grade) / 3 - 0.5

df1 = pd.read_csv("../data/LSTM-比特币.csv")
df2 = pd.read_csv("../data/灰色涨幅-比特币.csv", delimiter = ',')
lstm_grade = np.array(df1.values[:, 1], dtype = float) # 序列: 所有的0,1串
days = len(lstm_grade)
gray_list = np.array(df2.values[:, 1], dtype = float) # 涨幅
rsi = Rsi.get_rsi_list() # rsi指标天数
ic(len(lstm_grade))
ic(len(gray_list))
ic(len(rsi))
ic(gray_list)
tran_days = Macd.get_tran_days()
rsi_grade = get_rsi_grade(rsi)
gray_grade = get_gray_grade(gray_list)

ic(len(gray_grade))
ic(len(rsi_grade))

overall_grade = np.zeros((days, ))
for day in range(days):
    for i in range(days):
        overall_grade[i] = get_overall_grade(lstm_grade[i], gray_grade[i], rsi_grade[i])

ic(overall_grade)
np.savetxt("../data/综合指标-比特币.csv", overall_grade)