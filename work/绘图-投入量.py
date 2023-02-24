"""
投入量与结果的关系
"""

import pandas as pd
import matplotlib.pyplot as plt

from icecream import ic

df = pd.read_csv("../data/每次投入量.csv")

plt.plot(df.values[:,0], df.values[:,1])
plt.show()