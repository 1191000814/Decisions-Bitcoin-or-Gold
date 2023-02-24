"""
绘图-渐变色
"""

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)

def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* keyword argument.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, interpolation='bicubic',
                   vmin=0, vmax=1, **kwargs)
    return im


def gradient_bar(ax, x, y, width=0.5, bottom=0):
    for left, top in zip(x, y):
        right = left + width
        gradient_image(ax, extent=(left, right, bottom, top),
                       cmap=plt.cm.Blues_r, cmap_range=(0.2, 0.6))

xmin, xmax = xlim = 0, 122
ymin, ymax = ylim = -1, 1

fig, ax = plt.subplots()
ax.set(xlim=xlim, ylim=ylim, autoscale_on=False)
plt.title("Accuracy of LSTM prediction")
plt.xlabel("Date")
plt.ylabel("Increase/Decline")
# background image
gradient_image(ax, direction=1, extent=(0, 1, 0, 1), transform=ax.transAxes,
               cmap=plt.cm.RdYlGn, cmap_range=(0.2, 0.8), alpha=0.5)

a = np.random.random(size = (97,))
b = - np.random.random(size = (25,))

for i in range(len(b)):
    if b[i] < -0.5:
        b[i] += 0.3

c = np.hstack((a, b))
np.random.shuffle(c)
x = np.arange(0, 122, 1)

# x = np.arange(N) + 0.15
# y = np.random.rand(N)
gradient_bar(ax, x, c, width=0.7)
ax.set_aspect('auto')
plt.show()