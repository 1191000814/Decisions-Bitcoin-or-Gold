"""
预测比特币
"""

from MACD import Macd
from Trading import Trading
from icecream import ic

import numpy as np
import matplotlib.pyplot as plt

ema12 = Macd.ema(12)
ema26 = Macd.ema(26)
dif_list = Macd.dif()
dea_list = Macd.dea()
macd_list = Macd.macd()

ic(ema12)
ic(ema26)
ic(dif_list)
ic(macd_list)
ic(dea_list)

capital_list = np.zeros((Trading.DAYS,))
trading = Trading()
trading.capital[1] = 900
overall_grade = np.loadtxt("../data/综合指标-比特币.csv", encoding = "UTF-8") # 三种因素得到的综合评价指标

for day in range(Trading.DAYS - 1):
    trading.day = day
    if (macd_list[day] < 0) & (macd_list[day + 1] > 0):  # 由负变正->买
        trading.tran(trading.capital[1] * Trading.TRAN_SCALE *
                     (1 + Trading.FACTOR_WEIGHT * overall_grade[day]))
    elif (macd_list[day] > 0) & (macd_list[day + 1] < 0):  # 由正变负->卖
        trading.tran(-trading.capital[3] * Trading.BTC_VALUE[day] *
                     Trading.TRAN_SCALE * (1 - Trading.FACTOR_WEIGHT * overall_grade[day]))
    # print(trading.capital)
    capital_list[day] = trading.get_asset()

ic(np.sum(trading.tran_num))
ic(trading.capital)
ic(trading.get_asset())
np.savetxt("../data/买卖数量.csv", trading.tran_num)
np.savetxt("../data/资产值变化.csv", capital_list)
x = np.arange(Trading.DAYS)
plt.plot(x[:900], capital_list[:900])
plt.show()