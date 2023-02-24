"""
灰色预测-马尔科夫预测模型
"""

import numpy as np

from icecream import ic

TRAIN_NUM = 3 # 训练的数量
ERROR_BORDER1 = 0.001 # 误差的界限1
ERROR_BORDER2 = 0.002 # 界面2
FINAL_ERRORS = [0.003, 0.0015, 0.0005, -0.0005, -0.0015, -0.003] # 最终目标误差
FORECAST_NUM = 10 # 用多少个样本预测一个样本
STATE_NUM = 6 # 状态数

forecast = np.loadtxt("../data/灰色预测-预测值.txt")
errors = np.loadtxt("../data/灰色预测-相对误差.txt")

def get_states(error):
    """
    判断误差区间
    """
    if error > ERROR_BORDER2:
        return 0
    elif (error > ERROR_BORDER1) & (error < ERROR_BORDER2):
        return 1
    elif (error > 0) & (error < ERROR_BORDER1):
        return 2
    elif (error < 0) & (error > -ERROR_BORDER1):
        return 3
    elif (error < -ERROR_BORDER1) & (error > -2 * ERROR_BORDER2):
        return 4
    else:
        return 5


def get_error(index):
    """
    根据索引获取精确后的误差值
    根据前四个区间, 得到第五个的预测的修改值
    """
    pre_errors = errors[index - FORECAST_NUM : index] # 前几个误差值
    pro_transfer = get_probability(index) # 转移矩阵
    pro_transfers = np.zeros((FORECAST_NUM, STATE_NUM, STATE_NUM)) # 转移矩阵的次方
    pro_states = np.zeros((STATE_NUM, 1)) # 概率矩阵
    pro_transfers[0] = pro_transfer

    for i in range(FORECAST_NUM):
        pro_transfers[i] *= pro_transfer

    for i in range(len(pre_errors)):
        pre_errors[i] = get_states(pre_errors[i]) # 转化为区间

    for i in range(STATE_NUM): # 分别计算每个区间的概率
        for j in range(FORECAST_NUM): # 分别对前四天到该状态的概率相加
            pro_states[i] += pro_transfers[FORECAST_NUM - j - 1][get_states(pre_errors[j]), i]

    # 求出概率最大的区间
    max_i = 0
    for i in range(4):
        if pro_states[i] > pro_states[max_i]:
            max_i = i
    return FINAL_ERRORS[get_states(max_i)]


def get_probability(index):
    """
    根据索引, 获取概率矩阵
    """
    train_data = errors[index - TRAIN_NUM - 1 : index] # 误差的训练数据
    probability = np.zeros((STATE_NUM, STATE_NUM)) # 概率矩阵

    for i in range(TRAIN_NUM): # 确定概率矩阵
        probability[get_states(train_data[i]), get_states(train_data[i + 1])] += 1

    for i in range(STATE_NUM): # 概率矩阵归一化
        if probability.sum(axis = 1)[i] > 0:
            probability[i] /= probability.sum(axis = 1)[i]

    return probability

# 状态1: <-2

states = np.ones(errors.shape) # 各个区间的状态
for i in range(len(errors)):
    states = get_states(errors[i])

ic(forecast)
ic(errors)

n = len(forecast)

# 遍历每四个数据求出第五天应该是哪个区间
for i in range(FORECAST_NUM + 1, n):
    error = get_error(i)
    forecast[i] /= (1 + 0.1 * error)
ic(forecast)

np.savetxt("../data/修改误差.csv", forecast)
pre_error = np.loadtxt("../data/原相对误差.csv")
origin_data = np.loadtxt("../data/初始值.csv")

ic(np.sum(np.abs(pre_error)))
new_error = (forecast - origin_data) / origin_data
ic(np.sum(np.abs(new_error)))