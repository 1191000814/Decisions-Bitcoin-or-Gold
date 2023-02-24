"""
计算 macd
"""

import numpy as np

from work.Trading import Trading

class Macd:

    RELATE_DAYS = 9
    LONG_DAYS = 26
    SHORT_DAYS = 12
    MAX_BIAS = 0.15 # 比特币乖离值达到多少时,要考虑买黄金
    BIAS_DAYS = 15 # 乖离值考虑的天数

    @staticmethod
    def ema(n, form = True):
        """
        计算加权均线 EMA
        n: 多少日的ema, 12或者16
        form: 是否是比特币
        """
        ema_list = np.zeros((Trading.DAYS,))
        if form is True: # 是比特币
            value = Trading.BTC_VALUE
        else:
            value = Trading.GOLD_VALUE
        ema_list[0] = value[0]
        for i in range(1, len(ema_list)):
            ema_list[i] = (n - 1) / (n + 1) * ema_list[i - 1] + 2 / (n + 1) * value[i]
        return ema_list

    @staticmethod
    def dif(form = True):
        """
        计算离差值DIF
        """
        return Macd.ema(12, form) - Macd.ema(26, form)

    @staticmethod
    def dea(form = True):
        """
        九日均线DEA值
        """
        dea_list = np.zeros((Trading.DAYS,))
        dif_list = Macd.dif(form)
        dea_list[0] = 0
        for i in range(1, Trading.DAYS):
            dea_list[i] = dea_list[i - 1] * (Macd.RELATE_DAYS - 1) / (Macd.RELATE_DAYS + 1) + dif_list[i] * 2 / (
                        Macd.RELATE_DAYS + 1)
        return dea_list

    @staticmethod
    def macd(form = True):
        """
        指数平滑移动平均线 MACD
        """
        return 2 * (Macd.dif(form) - Macd.dea(form))

    @staticmethod
    def get_tran_days(form = True):
        """
        根据macd指标获取所有可以交易的天数
        买为1, 卖为-1, 不交易为0
        """
        macd_list = Macd.macd(form)
        days = len(macd_list)
        tran_days = np.zeros((days,))
        for day in range(1, days): # 无法预测未来一天是否能买
            if (macd_list[day - 1] < 0) & (macd_list[day] > 0) & ((form is True) | (Trading.GOLD_TRAN[day] == 1)):  # 由负变正->买
                tran_days[day] = 1
            elif (macd_list[day - 1] > 0) & (macd_list[day] < 0) & ((form is True) | (Trading.GOLD_TRAN[day] == 1)):  # 由负正变负->卖
                tran_days[day] = -1

        return tran_days

    @staticmethod
    def get_bias():
        """
        获取比特币乖离值数组
        乖离率=[(当日收盘价-N日平均价)/N日平均价] * 100%
        """
        value = Trading.BTC_VALUE
        bias_list = np.zeros((Trading.DAYS,))
        for day in range(Macd.BIAS_DAYS, Trading.DAYS):
            bias_mean = np.mean(value[day - Macd.BIAS_DAYS : day])
            bias_list[day] = (value[day] - bias_mean) / bias_mean
        return bias_list