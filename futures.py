# coding=utf-8

from pyecharts import Kline
from flask import Flask, render_template, request
import tushare as ts

from abupy.MarketBu.ABuSymbolFutures import AbuFuturesCn,AbuFuturesGB


class FuturesList(object):

    futuresCnList=AbuFuturesCn()