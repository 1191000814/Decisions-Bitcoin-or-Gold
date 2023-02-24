"""
工具包
"""
import numpy as np
import pandas as pd
import datetime

class Trading:
    """
    工具类包
    """
    TRAN_MONEY = 1000  # 每次买/卖的量(美元)
    TRAN_SCALE = 0.92 # 每次买/卖占总金额的比重
    FACTOR_WEIGHT = 0.2 # 综合指标占的权重
    DAY_INTERVAL = 20  # 每次买/卖的间隔
    START_DAY = 90  # 哪天开始买卖(从0开始)
    GOLD_RATE = 0.01  # 黄金交易率
    BTC_RATE = 0.02  # 比特币交易率
    ALL_DATA = pd.read_csv("../data/黄金-比特币价值.csv", index_col = 0)
    BTC_VALUE = np.array(ALL_DATA.values[:, 2], dtype = float) # 比特币价值
    GOLD_VALUE = np.array(ALL_DATA.values[:, 1], dtype = float) # 黄金价值
    GOLD_TRAN = np.array(ALL_DATA.values[:, 3], dtype = int) # 黄金可交易的天数
    DAYS = len(BTC_VALUE)  # 总天数

    def __init__(self):
        self.capital = np.array([100, 900, 0, 0], dtype = float)
        # 当前资产: [用来买黄金的美元, 用来买比特币的美元, 黄金, 比特币]
        self.tran_num = np.zeros((Trading.DAYS, )) # 每天交易的金额
        self.day = 0

    @staticmethod
    def get_date_list():
        """
        获取日期列表
        """
        d = datetime.date(year = 2016, month = 9, day = 11)
        return np.array([(d + datetime.timedelta(i)) for i in range(Trading.DAYS)])

    @staticmethod
    def get_interval_date():
        """
        获取有间隔的日期列表
        """


    def get_asset(self):
        """
        获取当前资产,全部换算成美元
        """
        return self.capital[0] + self.capital[1] + self.capital[2] * Trading.GOLD_VALUE[self.day] + self.capital[3] * Trading.BTC_VALUE[self.day]

    def tran(self, money, form = 3):
        """
        进行一次交易
        day: 交易天数
        money: 交易的美元数,正为买,负为卖
        capital: 当前资产
        form: 2为黄金交易, 3为比特币交易
        """
        if form == 3:
            value = Trading.BTC_VALUE[self.day]  # 当天比特币的价格
            rate = Trading.BTC_RATE
        else:
            value = Trading.GOLD_VALUE[self.day] # 当天的黄金价格
            rate = Trading.GOLD_RATE

        if ((money > 0) & (self.capital[form - 2] > money)) | ((money < 0) & (self.capital[form] > float(-money / value))):
            # 美元或者比特币是否还够用, 够用就买对应数量
            self.capital[form - 2] -= money
            self.capital[form] += money * (1 - rate) / value
            self.tran_num[self.day] = money
        elif money > 0:
            # 美元不够用时, 全部买掉
            self.tran_num[self.day] = self.capital[form - 2]
            self.capital[form] += self.capital[form - 2] * (1 - rate) / value
            self.capital[form - 2] = 0  # 美元清空
        elif money < 0:
            # 比特币不够用时, 全部卖掉
            self.tran_num[self.day] = self.capital[form]
            self.capital[form - 2] += self.capital[form] * value * (1 - rate)
            self.capital[form] = 0