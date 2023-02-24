"""
随机提前或推迟的影响
"""

import matplotlib.pyplot as plt
import numpy as np
from work.Trading import Trading
from icecream import ic

LINE_WIDTH = 1
START_DAY = 1200

c0 = np.loadtxt("../data/资产值变化-最终版本.csv")[:-1]
c1 = np.loadtxt("../data/资产值变化-随机提前或推迟一天.csv")[:-1]
c3 = np.loadtxt("../data/资产值变化-随机提前或推迟3天.csv")[:-1]
c5 = np.loadtxt("../data/资产值变化-随机提前或推迟5天.csv")[:-1]

date = Trading.get_date_list()[:-1]
x = np.arange(Trading.DAYS - 1)

plt.plot(date[START_DAY:], c0[START_DAY:], label="normal", linewidth=LINE_WIDTH)
plt.plot(date[START_DAY:], c1[START_DAY:], label="randomly delay or in advance 1 day", linewidth=LINE_WIDTH)
plt.plot(date[START_DAY:], c3[START_DAY:], label="randomly delay or in advance 3 day", linewidth=LINE_WIDTH)
plt.plot(date[START_DAY:], c5[START_DAY:], label="randomly delay or in advance 5 day", linewidth=LINE_WIDTH)

plt.title("Revenue varies when postpone or advance by a few days randomly")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.grid()
plt.show()