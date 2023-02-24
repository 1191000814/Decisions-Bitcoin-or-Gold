"""
计算年化收益率
"""

"""
MACD决策-- 黄金+比特币, 考虑乖离值
"""

import numpy as np
from MACD决策_返回值版 import my_macd
from MACD import Macd
from icecream import ic

ic(my_macd())
ic((my_macd() / 1000) / 1826 * 365)
