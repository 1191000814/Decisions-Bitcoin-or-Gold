"""
固定一个维度, 分析另一个
"""

import matplotlib.pyplot as plt
import numpy as np
from icecream import ic

a = np.loadtxt("../data/根据交易率变化的数据.csv")
ic(a.shape)

x = np.arange(0.05, 0.15, 0.005)
# y = np.arange(0.1, 0.3, 0.01)
plt.plot(x, a[10, :])
# plt.plot(y, a[:, 10])
plt.show()

for i in range(19):
    ic((a[10][i + 1] - a[10][i]) / 0.005)

for i in range(19):
    ic((a[i][10] - a[i + 1][10]) / 0.01)