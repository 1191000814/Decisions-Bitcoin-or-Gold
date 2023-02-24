"""
macd
"""

import numpy as np
import matplotlib.pyplot as plt

from work.MACD import Macd
from work.Trading import Trading

START_DAY = 1500
END_DAY = 1800
LINE_WIDTH = 0.5

if __name__ == '__main__':

    ema12 = Macd.ema(12)
    ema26 = Macd.ema(26)
    dif_list = Macd.dif()
    dea_list = Macd.dea()
    macd_list = Macd.macd()
    colors = ['' for _ in range(len(macd_list))]
    for i in range(len(macd_list)):
        if macd_list[i] >= 0:
            colors[i] = 'r'
        else:
            colors[i] = 'g'

    date = Trading.get_date_list()[: -1]
    x = np.arange(Trading.DAYS)
    plt.figure(figsize = (60, 40), dpi = 120)
    # plt.ylim(0, 7000)
    plt.plot(date[START_DAY:END_DAY], Trading.BTC_VALUE[START_DAY:END_DAY] / 10, color = "y", label = "btc_price",
             linewidth = LINE_WIDTH)
    # plt.plot(x[START_DAY:END_DAY], Rsi.get_rsi_list(), color="g", label="rsi")
    plt.plot(date[START_DAY:END_DAY], dif_list[START_DAY:END_DAY], "r", label = "dif", linewidth = LINE_WIDTH)
    plt.plot(date[START_DAY:END_DAY], dea_list[START_DAY:END_DAY], "b", label = "dea", linewidth = LINE_WIDTH)
    plt.bar(date[START_DAY:END_DAY], macd_list[START_DAY:END_DAY], color = colors[START_DAY:END_DAY], label = "macd")
    plt.title("macd, dea, dif indicators and bitcoin price")
    plt.xlabel("date")
    plt.ylabel("value")
    plt.legend()
    plt.grid()
    plt.show()