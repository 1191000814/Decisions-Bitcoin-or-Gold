"""
main
"""
import random
import datetime

import matplotlib.pyplot as plt
import numpy as np

from Trading import Trading
from MACD import Macd
from icecream import ic

# ic(Trading.BTC_VALUE)
# ic(len(Trading.BTC_VALUE))
# ic(Trading.GOLD_VALUE)
# ic(len(Trading.GOLD_VALUE))
# ic(Trading.GOLD_TRAN)
# ic(Macd.get_bias())

from datetime import date

d = datetime.date(year = 2016, month = 9, day = 11)
print(d.strftime("%y/%m/%d"))
print(d - datetime.timedelta(1))

print(len(Trading.get_date_list()))