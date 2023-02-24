"""
预测黄金
"""

from MACD import Macd
from Trading import Trading
from icecream import ic

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ema12 = Macd.ema(12, False)
    ema26 = Macd.ema(26, False)
    dif_list = Macd.dif(False)
    dea_list = Macd.dea(False)
    macd_list = Macd.macd(False)

    ic(ema12)
    ic(ema26)
    ic(dif_list)
    ic(macd_list)
    ic(dea_list)

    capital_list = np.zeros((Trading.DAYS,))
    trading = Trading()
    for day in range(Trading.DAYS - 1):
        trading.day = day
        if Trading.GOLD_TRAN[day] == 0: # 该天黄金不可见交易
            continue
        elif (macd_list[day] < 0) & (macd_list[day + 1] > 0):  # 由正变负->买
            trading.tran(trading.capital[0] * Trading.TRAN_SCALE)
        elif (macd_list[day] > 0) & (macd_list[day + 1] < 0):  # 由负变正->卖
            trading.tran(-trading.capital[1] * Trading.GOLD_VALUE[day] * Trading.TRAN_SCALE)
        print(trading.capital)
        capital_list[day] = trading.get_asset()

    ic(np.sum(trading.tran_num))
    ic(trading.capital)
    ic(trading.get_asset())
    np.savetxt("./data/买卖数量.csv", trading.tran_num)
    # np.savetxt("./data/rsi.csv", rsi)
    # np.savetxt("./data/买点.csv", buy)
    x = np.arange(Trading.DAYS)
    plt.plot(x[:600], capital_list[:600])
    plt.show()