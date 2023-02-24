"""
测试版本
"""

from MACD import Macd
from Trading import Trading
from icecream import ic

import numpy as np

CHANGE_RATE = 0.01

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
bias_list = Macd.get_bias() # 乖离值

gold_day = 0 # 黄金买卖的多少天
# 因为综合指标只记了黄金能买卖的天数, 而其他的都是全天数
flow_capital = 0 # 从比特币转移到黄金去的资金

for day in range(Trading.DAYS - 1):
    trading.day = day
    # 黄金买卖策略
    # 注意买卖的知识黄金的部分
    if Trading.GOLD_TRAN[day] == 1:
        if (macd_gold[day] < 0) & (macd_gold[day + 1] > 0):  # 比特币: 由负变正->买
            money = trading.capital[0] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
            trading.tran(money * (1 + CHANGE_RATE), 2)
        elif (macd_gold[day] > 0) & (macd_gold[day + 1] < 0):  # 比特币: 由正变负->卖
            money = -trading.capital[2] * Trading.GOLD_VALUE[day] * Trading.TRAN_SCALE * (1 - Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
            trading.tran(money * (1 + CHANGE_RATE), 2)
        gold_day += 1

    # 比特币买卖策略
    if (macd_btc[day] < 0) & (macd_btc[day + 1] > 0):  # 比特币: 由负变正->买
        if bias_list[day] > Macd.MAX_BIAS:  # 乖离值过大
            money = 1 / 2 * trading.capital[1] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * btc_overall_grade[day])
            # 只用计划资金的一半用来购买比特币, 另一半购买黄金
            trading.tran(money * (1 + CHANGE_RATE))
            if Trading.GOLD_TRAN[day] == 1: # 可以购买黄金就买
                trading.tran(money * (1 + CHANGE_RATE), 2)
            else: # 否则就放在用来购买黄金的资金里
                trading.capital[0] += money
                trading.capital[1] -= money
                flow_capital += money
        else: # 乖离值正常
            if flow_capital > 0: # 如果有流动资金
                temp = min(flow_capital, trading.capital[0])
                trading.capital[0] -= temp
                trading.capital[1] += temp
                flow_capital -= temp
            money = trading.capital[1] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * btc_overall_grade[day])
            trading.tran(money * (1 + CHANGE_RATE))
    elif (macd_btc[day] > 0) & (macd_btc[day + 1] < 0):  # 比特币: 由正变负->卖
        money = -trading.capital[3] * Trading.BTC_VALUE[day] * Trading.TRAN_SCALE * (1 - Trading.FACTOR_WEIGHT * btc_overall_grade[day])
        trading.tran(money * (1 + CHANGE_RATE))
    capital_list[day] = trading.get_asset()

ic(np.sum(trading.tran_num))
ic(trading.capital)
ic(trading.get_asset())
# np.savetxt("../data/买卖数量.csv", trading.tran_num)
np.savetxt("../data/资产值变化-偏大版.csv", capital_list)
x = np.arange(Trading.DAYS)
# plt.plot(x[:900], capital_list[:900])
# plt.show()