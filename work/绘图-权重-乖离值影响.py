"""
资产走势
"""

import matplotlib.pyplot as plt
import numpy as np

from work.Trading import Trading

c1 = np.loadtxt("../data/资产值变化-最终版本.csv")[:-1]
c2 = np.loadtxt("../data/资产值变化-不考虑权重.csv")[:-1]
c3 = np.loadtxt("../data/资产值变化-偏大版.csv")[:-1]
c4 = np.loadtxt("../data/资产值变化-偏小版.csv")[:-1]

c = [c1, c2, c3]
x = Trading.get_date_list()[:-1]

plt.plot(x[1200:], c1[1200:], color='g', label="ultimate model", linewidth=1)
plt.plot(x[1200:], c2[1200:], color='b', label="Regardless of evaluate weight", linewidth=1)
plt.plot(x[1200:], c3[1200:], color='y', label="trade a little less than normal", linewidth=1)
plt.plot(x[1200:], c4[1200:], color='r', label="trade a little more than normal", linewidth=1)
plt.title("Change the amount of each trade, the final change in returns")
plt.grid()
plt.legend()
plt.xlabel("date")
plt.ylabel("the all asset")
plt.xticks()
plt.show()