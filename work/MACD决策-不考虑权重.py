"""
MACD决策-- 黄金+比特币
"""

from MACD import Macd
from Trading import Trading
from icecream import ic

import numpy as np
import matplotlib.pyplot as plt

# 比特币指标
ema12_btc = Macd.ema(12)
ema26_btc = Macd.ema(26)
dif_btc = Macd.dif()
dea_btc = Macd.dea()
macd_btc = Macd.macd()

# 黄金指标
ema12_gold = Macd.ema(12, False)
ema26_gold = Macd.ema(26, False)
dif_gold = Macd.dif(False)
dea_gold = Macd.dea(False)
macd_gold = Macd.macd(False)

capital_list = np.zeros((Trading.DAYS,))
trading = Trading()
# [用来买黄金的美元, 用来买比特币的美元, 黄金, 比特币]

gold_overall_grade = np.loadtxt("../data/综合指标-黄金.csv") # 三种因素得到的综合评价指标
btc_overall_grade = np.loadtxt("../data/综合指标-比特币.csv")
tran_days = Macd.get_tran_days()

gold_day = 0 # 黄金买卖的多少天
# 因为综合指标只记了黄金能买卖的天数, 而其他的都是全天数
for day in range(Trading.DAYS - 1):
    trading.day = day
    # 黄金买卖策略
    # 注意买卖的知识黄金的部分
    if Trading.GOLD_TRAN[day] == 1:
        if (macd_gold[day] < 0) & (macd_gold[day] > 0):  # 比特币: 由负变正->买
            money = trading.capital[0] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
            trading.tran(money, 2)
        elif (macd_gold[day] > 0) & (macd_gold[day + 1] < 0):  # 比特币: 由正变负->卖
            money = -trading.capital[2] * Trading.GOLD_VALUE[day] * Trading.TRAN_SCALE * (1 - Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
            trading.tran(money, 2)
        gold_day += 1

    # 比特币买卖策略
    if (macd_btc[day] < 0) & (macd_btc[day + 1] > 0):  # 比特币: 由负变正->买
        money = trading.capital[1]
        trading.tran(money)
    elif (macd_btc[day] > 0) & (macd_btc[day + 1] < 0):  # 比特币: 由正变负->卖
        money = -trading.capital[3] * Trading.BTC_VALUE[day]
        trading.tran(money)
    # ic(trading.capital)
    capital_list[day] = trading.get_asset()

ic(np.sum(trading.tran_num))
ic(trading.capital)
ic(trading.get_asset())
# np.savetxt("../data/买卖数量.csv", trading.tran_num)
np.savetxt("../data/资产值变化-不考虑权重.csv", capital_list)
x = np.arange(Trading.DAYS)
# plt.plot(x[:900], capital_list[:900])
# plt.show()