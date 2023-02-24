"""
乖离率
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from icecream import ic
from work.MACD import Macd

START_DAY = 0
END_DAY = 1800
HIGH = 0.625

bias_list = Macd.get_bias()
capital = pd.read_csv("../data/资产值变化.csv").values / 4 * 10 ** 6
days = len(bias_list)

ic(bias_list)
ic(capital)
y = np.ones((days,)) * 0.625
high = [] # 高于0.625的日期

high_value = []
for x in high:
    high_value.append(capital[x])

x = np.arange(days)
# plt.scatter(high, high_value)
# plt.plot(x[START_DAY:END_DAY], gl[START_DAY:END_DAY], label="bias")
plt.plot(x[START_DAY:END_DAY], capital[START_DAY:END_DAY] / 5e11, label="capital", color="y")
# plt.plot(x[START_DAY:END_DAY], y[START_DAY:END_DAY], label=str(HIGH))
plt.plot(x[START_DAY:END_DAY], bias_list[START_DAY:END_DAY], label="bias")
plt.legend()
plt.show()