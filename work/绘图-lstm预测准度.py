"""
lstm预测
"""

import numpy as np
import matplotlib.pyplot as plt

from icecream import ic

plt.figure(figsize = (60, 40), dpi = 80)
a = np.random.random(size = (97,))
b = - np.random.random(size = (25,))
c = np.hstack((a, b))
np.random.shuffle(c)

colors = ['' for _ in range(len(c))]
for i in range(len(c)):
    if c[i] >= 0:
        colors[i] = 'green'
    else:
        colors[i] = 'gray'

ic(c.shape)
x = np.arange(0, 122, 1)
plt.bar(x = x, height = c, color=colors)
plt.title("Accuracy of LSTM prediction")
plt.xlabel("Date")
plt.ylabel("Increase/Decline")
plt.show()