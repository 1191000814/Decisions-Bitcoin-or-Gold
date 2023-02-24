"""
投资计算结果
"""

import numpy as np
import pandas as pd

from icecream import ic

N = 1827 # 天数

asset = np.array([1000, 0, 0]) # 资产
invest = np.zeros((2, N)) # 投资, 买入为正, 卖出为负
gold_price = pd.read_csv("../data/黄金价值.csv")
btc_price = pd.read_csv("../data/比特币价值.csv")

ic(type(btc_price["Date"]))

ic(gold_price)