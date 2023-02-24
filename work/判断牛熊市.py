"""
判断牛熊市
"""
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

# data.to_csv('000001.csv')
# data = pd.read_csv('000001.csv')  # 为防止意外可以先将数据储存下来
def get_bull_or_bear(series, order = 100):
    '''
    获取时间区间所处的牛熊市状态
    传入: series如close, order代表划分前后追朔的数据量,数据量越大,精度越小
    返回: 交易日的牛熊市的分类，series
    '''

    # 利用scipy在前后order个交易日内寻找极值点
    x = series.values
    high = argrelextrema(x, np.greater, order = order)[0]
    # argrelextrema: 寻找离散数据的极值点
    low = argrelextrema(x, np.less, order = order)[0]

    high_s = pd.Series('high', series.iloc[high].index)
    low_s = pd.Series('low', series.iloc[low].index)

    data1 = pd.concat([high_s, low_s]).sort_index()
    other = []
    for i in range(len(data1) - 1):  # 去除重复值划分
        if data1.iloc[i] == data1.iloc[i + 1]:
            other.append(data1.index[i])
    data1.drop(other, inplace = True)

    data1[series.index[-1]] = data1.iloc[-2]  # 加上开头与结束的归类
    data1[series.index[0]] = data1.iloc[1]
    data1.sort_index(inplace = True)  # 获得牛熊分界点

    bull_data = pd.Series(False, series.index, name = 'is_bull')  # 获得每一交易日属于牛市期还是熊市期
    if data1[0] == 'high':
        is_bull = False
    else:
        is_bull = True
    for i in range(len(data1) - 1):
        if is_bull:
            bull_data[data1.index[i]:data1.index[i + 1]] = True
            is_bull = False
        else:
            is_bull = True
    return bull_data

# bull_data = get_bull_or_bear(data.close, 100)
# bull_data.value_counts()
df = pd.DataFrame(np.array([1, 2, 3, 4, 5]))
bull_data = get_bull_or_bear(df, 100)
print(bull_data)

# False
# 1761
# True
# 1128
# Name: is_bull, dtype: int64
# ax = bull_data.plot(style = '-', figsize = (17, 5))
# data.close.plot(secondary_y = True, ax = ax)