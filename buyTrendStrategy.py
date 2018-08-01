# -*- encoding:utf-8 -*-
"""
    测试购买因子
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys



from abupy import ABuSymbolPd
from abupy import AbuFactorBuyBreak
# from abupy import AbuFactorBuyBreak
from abupy import AbuBenchmark , AbuCapital

from abupy import ABuPickTimeExecute
from abupy.AlphaBu.ABuPickTimeWorker import AbuPickTimeWorker


class BuyTrendStrategy(object):

    def __init__(self,symbol,period,money):

        self.symbol = symbol
        self.buy_factors = [{'xd': period, 'class': AbuFactorBuyBreak}]
        self.benchmark = AbuBenchmark()
        self.capital=AbuCapital(money,self.benchmark)

    def get_close_line(self):

        self.kl_df = ABuSymbolPd.make_kl_df( self.symbol ,n_folds=2)
        closeValueList = self.kl_df["close"].values.tolist()
        closeDayList = self.kl_df["close"].index.tolist()
        closeDayList = [str(i.strftime("%Y%m%d")) for i in closeDayList]
        return closeDayList,closeValueList

    def get_buy_point(self):

        ptw = AbuPickTimeWorker(self.capital, self.kl_df, self.benchmark, self.buy_factors, None)
        ptw.fit()
        buyDayList = [str(i.buy_date) for i in ptw.orders]
        buyValueList = [i.buy_price for i in ptw.orders]

        return buyDayList,buyValueList


