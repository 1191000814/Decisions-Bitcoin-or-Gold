"""
价值-买卖点
"""

import numpy as np
import matplotlib.pyplot as plt

from work.MACD import Macd
from work.Trading import Trading

START_DAY = 300
END_DAY = 600

if __name__ == '__main__':

    x = np.arange(START_DAY, END_DAY, 1)
    plt.plot(x, Trading.BTC_VALUE[START_DAY:END_DAY], color="y")
    tran_days = Macd.get_tran_days()
    buy_days = []
    sell_days = []
    for day in range(START_DAY, END_DAY):
        if tran_days[day] == 1:  # 买点
            buy_days.append(day)
        elif tran_days[day] == -1:  # 卖点
            sell_days.append(day)

    buy_values = [0 for _ in range(len(buy_days))]
    sell_values = [0 for _ in range(len(sell_days))]
    date = Trading.get_date_list()[:-1]

    i = 0
    for day in buy_days:
        buy_values[i] = Trading.BTC_VALUE[day]
        i += 1
    i = 0
    for day in sell_days:
        sell_values[i] = Trading.BTC_VALUE[day]
        i += 1

    plt.scatter(buy_days, buy_values, color="g", cmap = "*")
    plt.scatter(sell_days, sell_values, color="r", cmap = ".")
    plt.show()