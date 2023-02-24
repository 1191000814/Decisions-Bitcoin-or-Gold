"""
RSI决策

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from icecream import ic
from Trading import Trading

class Rsi:
    """
    RSI决策
    """

    RSI_NUM = 15  # rsi每次判断需要的天数

    @staticmethod
    def get_rsi(day, form = True):
        """
        index: 天数
        返回rsi系数
        """
        assert day >= Rsi.RSI_NUM # 确保有足够的天数可以预测
        if form is True:
            refer = Trading.BTC_VALUE[day - Rsi.RSI_NUM - 1: day]  # rsi参考的天数
        else:
            refer = Trading.GOLD_VALUE[day - Rsi.RSI_NUM - 1: day]
        add_num = 0
        sub_num = 0
        for i in range(len(refer) - 1):
            if refer[i + 1] > refer[i]:
                add_num = refer[i + 1] - refer[i]
            elif refer[i + 1] < refer[i]:
                sub_num = refer[i] - refer[i + 1]
        return add_num / (add_num + sub_num)

    @staticmethod
    def get_rsi_list(form = True):
        """
        求出rsi列表
        """
        if form is True:
            days = Trading.DAYS
        else:
            days = Trading.GOLD_DAYS
        rsi_list = np.zeros((days, ))
        for day in range(Rsi.RSI_NUM + 1, days):
            rsi_list[day] = Rsi.get_rsi(day, form)
        return rsi_list

if __name__ == '__main__':
    btc = pd.read_csv("../data/比特币价值.csv")
    btc_value = np.array(btc.values[:, 1], dtype = float)
    gold = pd.read_csv("../data/黄金价值.csv")
    gold_value = np.array(gold.values[:, 1], dtype = float)
    DAYS = len(btc_value)

    ic(DAYS)
    ic(btc_value) # 比特币的价值

    trading = Trading() # 交易对象

    # 循环处理每天的交易
    for day in range(90, DAYS, Trading.DAY_INTERVAL):
        rsi = Rsi.get_rsi(day) # 当天的rsi系数
        money = 0
        if rsi > 0.8: # 大于0.8, 考虑会反转, 卖出
            trading.tran(-Trading.BUY_MONEY)
        elif (rsi > 0.5) & (rsi <= 0.8): # 0.5-0.8, 平稳上升, 买入
            trading.tran(Trading.BUY_MONEY)
        elif (rsi > 0.2) & (rsi <= 0.5): # 0.2-0.5, 较为低迷, 卖出
            trading.tran(-Trading.BUY_MONEY)
        elif rsi <= 0.2: # 处于低谷, 买进
            trading.tran(Trading.BUY_MONEY)
        trading.day += 1

    ic(trading.get_asset())
    ic(trading.tran_num)

    plt.scatter(np.arange(DAYS), trading.tran_num)
    plt.plot(np.arange(DAYS), btc_value / 1000)
    plt.show()