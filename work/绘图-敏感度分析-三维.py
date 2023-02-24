"""
敏感度分析
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from work.MACD决策_返回值版 import my_macd
from icecream import ic

x = np.arange(0.005, 0.015, 0.0005)
y = np.arange(0.01, 0.03, 0.001)

ic(x.shape)
ic(y.shape)

X, Y = np.meshgrid(x, y)

Z = np.loadtxt("../data/根据交易率变化的数据.csv")
# Z = f(X, Y)
ic(Z.shape)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.view_init(60, 35)

ax.set_title('The result changes with the transaction rate')

# ax = plt.axes(projection='3d')
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('surface')

# r = np.linspace(0, 6, 20)
# theta = np.linspace(-0.9 * np.pi, 0.8 * np.pi, 40)
# r, theta = np.meshgrid(r, theta)

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')

plt.show()