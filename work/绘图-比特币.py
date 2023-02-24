"""
绘图
"""
import numpy as np
import matplotlib.pyplot as plt

from work.MACD import Macd
from work.RSI import Rsi
from work.Trading import Trading

if __name__ == '__main__':

    ema12 = Macd.ema(12)
    ema26 = Macd.ema(26)
    dif_list = Macd.dif()
    dea_list = Macd.dea()
    macd_list = Macd.macd()

    """保存文件"""
    # np.savetxt("../data/ema12.csv", ema12)
    # np.savetxt("../data/ema26.csv", ema26)
    # np.savetxt("../data/dif.csv", dif_list)
    # np.savetxt("../data/macd.csv", macd_list)

    buy_days = []
    sell_days = []
    for day in range(Trading.DAYS - 1):
        if (macd_list[day + 1] < 0) & (macd_list[day] > 0): # 买点
            buy_days.append(day + 1)
        elif (macd_list[day + 1] > 0) & (macd_list[day] < 0): # 卖点
            sell_days.append(day + 1)

    buy_points = np.arange(len(buy_days))
    sell_points = np.arange(len(sell_days))
    i = 0
    for day in buy_days:
        buy_points[i] = Trading.BTC_VALUE[day] / 5000
        i += 1
    i = 0
    for day in sell_days:
        sell_points[i] = Trading.BTC_VALUE[day] / 5000
        i += 1
    x = np.arange(Trading.DAYS)
    plt.figure(figsize = (60, 40), dpi = 120)
    plt.xlabel("date")
    plt.ylabel("value")
    plt.plot(x, Trading.BTC_VALUE / 5000, color="b", label="value")
    plt.plot(x, Rsi.get_rsi_list(), color="g", label="rsi")
    # plt.plot(x[1:300], dif_list[1:300], "r", label="dif")
    # plt.plot(x[1:300], dea_list[1:300], "b", label="dea")
    # plt.bar(x, macd_list, color="g", label="macd")

    for day in buy_days:
        plt.scatter(buy_days, buy_points, color="red", linewidths = 0.001)
    for day in sell_days:
        plt.scatter(sell_days, sell_points, color="green", linewidths = 0.001)

    plt.legend()
    plt.show()