"""
带有返回值可以调用
"""

from MACD import Macd
from Trading import Trading
from icecream import ic

import numpy as np

def my_macd(x1 = 0.01, x2 = 0.02):
    """
    x1: 黄金比率
    x2: 比特币比率
    """
    # 比特币指标
    macd_btc = Macd.macd()
    # 黄金指标
    macd_gold = Macd.macd(False)

    capital_list = np.zeros((Trading.DAYS,))
    trading = Trading()
    Trading.BTC_RATE = x1
    Trading.GOLD_RATE = x2
    # [用来买黄金的美元, 用来买比特币的美元, 黄金, 比特币]

    gold_overall_grade = np.loadtxt("../data/综合指标-黄金.csv")  # 三种因素得到的综合评价指标
    btc_overall_grade = np.loadtxt("../data/综合指标-比特币.csv")
    bias_list = Macd.get_bias()  # 乖离值

    gold_day = 0  # 黄金买卖的多少天
    # 因为综合指标只记了黄金能买卖的天数, 而其他的都是全天数
    flow_capital = 0  # 从比特币转移到黄金去的资金

    for day in range(Trading.DAYS - 1):
        trading.day = day
        # 黄金买卖策略
        # 注意买卖的知识黄金的部分
        if Trading.GOLD_TRAN[day] == 1:
            if (macd_gold[day] < 0) & (macd_gold[day] > 0):  # 比特币: 由负变正->买
                money = trading.capital[0] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
                trading.tran(money, 2)
            elif (macd_gold[day] > 0) & (macd_gold[day + 1] < 0):  # 比特币: 由正变负->卖
                money = -trading.capital[2] * Trading.GOLD_VALUE[day] * Trading.TRAN_SCALE * (
                    1 - Trading.FACTOR_WEIGHT * gold_overall_grade[gold_day])
                trading.tran(money, 2)
            gold_day += 1

        # 比特币买卖策略
        if (macd_btc[day] < 0) & (macd_btc[day + 1] > 0):  # 比特币: 由负变正->买
            if bias_list[day] > Macd.MAX_BIAS:  # 乖离值过大
                money = 1 / 2 * trading.capital[1] * Trading.TRAN_SCALE * (
                        1 + Trading.FACTOR_WEIGHT * btc_overall_grade[day])
                # 只用计划资金的一半用来购买比特币, 另一半购买黄金
                trading.tran(money)
                if Trading.GOLD_TRAN[day] == 1:  # 可以购买黄金就买
                    trading.tran(money, 2)
                else:  # 否则就放在用来购买黄金的资金里
                    trading.capital[0] += money
                    trading.capital[1] -= money
                    flow_capital += money
            else:  # 乖离值正常
                if flow_capital > 0:  # 如果有流动资金
                    temp = min(flow_capital, trading.capital[0])
                    trading.capital[0] -= temp
                    trading.capital[1] += temp
                    flow_capital -= temp
                money = trading.capital[1] * Trading.TRAN_SCALE * (1 + Trading.FACTOR_WEIGHT * btc_overall_grade[day])
                trading.tran(money)
        elif (macd_btc[day] > 0) & (macd_btc[day + 1] < 0):  # 比特币: 由正变负->卖
            money = -trading.capital[3] * Trading.BTC_VALUE[day] * Trading.TRAN_SCALE * (
                    1 - Trading.FACTOR_WEIGHT * btc_overall_grade[day])
            trading.tran(money)
        capital_list[day] = trading.get_asset()

    # ic(np.sum(trading.tran_num))
    # ic(trading.capital)
    # ic(trading.get_asset())
    # np.savetxt("../data/买卖数量.csv", trading.tran_num)
    # np.savetxt("../data/资产值变化-最终版本.csv", capital_list)
    x = np.arange(Trading.DAYS)
    # plt.plot(x[:900], capital_list[:900])
    # plt.show()
    return trading.get_asset()

if __name__ == '__main__':
    x1 = np.arange(0.005, 0.015, 0.0005)
    x2 = np.arange(0.01, 0.03, 0.001)
    values = np.zeros((len(x1), len(x2)))
    for i in range(len(x1)): # 黄金比率
        for j in range(len(x2)): # 比特币比率
            values[i, j] = my_macd(x1[i], x2[j])
    ic(values)
    np.savetxt("../data/根据交易率变化的数据.csv", values)