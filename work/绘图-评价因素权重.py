"""
评价因素权重
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/评价因子的权重.csv")

plt.plot(df.values[:,0], df.values[:,1])
plt.show()