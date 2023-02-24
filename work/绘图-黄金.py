"""
绘图--黄金
"""

import numpy as np
import matplotlib.pyplot as plt

from work.MACD import Macd
from work.Trading import Trading

if __name__ == '__main__':

    ema12 = Macd.ema(12, False)
    ema26 = Macd.ema(26, False)
    dif_list = Macd.dif(False)
    dea_list = Macd.dea(False)
    macd_list = Macd.macd(False)

    """保存文件"""
    # np.savetxt("../data/ema12.csv", ema12)
    # np.savetxt("../data/ema26.csv", ema26)
    # np.savetxt("../data/dif.csv", dif_list)
    # np.savetxt("../data/macd.csv", macd_list)

    x = np.arange(Trading.GOLD_DAYS)
    plt.figure(figsize = (60, 40), dpi = 120)
    plt.xlabel("date")
    plt.ylabel("value")
    plt.plot(x[601:1200], Trading.GOLD_VALUE[601:1200] / 50, color="b", label="value")
    # plt.plot(x, dif_list, "r", label="dif")
    # plt.plot(x, dea_list, "b", label="dea")
    plt.bar(x[601:1200], macd_list[601:1200], color="g", label="macd")

    plt.legend()
    plt.show()