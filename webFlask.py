# coding=utf-8
import random

from pyecharts import Kline,Line,EffectScatter,Overlap
from flask import Flask, render_template, request
import tushare as ts

from buyTrendStrategy import BuyTrendStrategy

app = Flask(__name__)

REMOTE_HOST = "https://pyecharts.github.io/assets/js"



@app.route("/")
def root1():
    return render_template("index.html")


@app.route("/waitting")
def waitting():
    return render_template("waitting.html")

@app.route("/futures")
def futures():
    return render_template("futures.html")


@app.route("/strategy")
def strategy():

    buyStrategy = BuyTrendStrategy('usTSLA',60,1000000)
    closeDayList, closeValueList = buyStrategy.get_close_line()
    buyDayList, buyValueList = buyStrategy.get_buy_point()

    closeLine = Line("趋势购买策略")
    closeLine.add("usTSLA", closeDayList, closeValueList)

    buyES = EffectScatter("购买点")
    buyES.add("购买点",buyDayList,buyValueList,symbol_size=16,effect_scale=5.5,effect_period=3,symbol="triangle")

    overlap = Overlap()
    overlap.add(closeLine)
    overlap.add(buyES)



    return render_template(
        "strategy.html",
        strategyEchart=overlap.render_embed(),
        host=REMOTE_HOST,
        script_list=buyES.get_js_dependencies(),
    )


@app.route("/mykline1")
def hello():
    kDate = getKdata('600606', '2018-06-01', '2018-07-01')


    kDay = [d[0] for d in kDate]
    kValue = [[x[1], x[2], x[3], x[4]] for x in kDate]

    kAll = [[x[0], x[1], x[2], x[3], x[4]] for x in kDate]

    kline = Kline('600606' + " K 线图", width="400", height="300")
    kline.add("日K", kDay, kValue)
    return render_template(
        "pyecharts.html",
        myechart=kline.render_embed(),
        host=REMOTE_HOST,
        script_list=kline.get_js_dependencies(),
        kAll=kAll
    )


@app.route("/mykline", methods=['POST'])
def mykline():
    form = request.form
    stock = form.get('stock')
    beginDay = form.get('beginDay')
    endDay = form.get('endDay')
    # print(stock)

    kDate = getKdata(stock, beginDay, endDay)
    # print(kDate)

    kDay = [d[0] for d in kDate]
    kValue = [[x[1], x[2], x[3], x[4]] for x in kDate]

    kAll = [[x[0], x[1], x[2], x[3], x[4]] for x in kDate]

    kline = Kline(str(stock) + " K 线图", width="400", height="300")
    kline.add("日K", kDay, kValue)
    return render_template(
        "pyecharts.html",
        myechart=kline.render_embed(),
        host=REMOTE_HOST,
        script_list=kline.get_js_dependencies(),
        kAll=kAll
    )





def getKdata(stocknumber, startdate, enddate, ):
    startdata = startdate.encode("ascii").replace("/", "-").replace("\n", "")  # convert to tushare readable date
    enddata = enddate.encode("ascii").replace("/", "-").replace("\n", "")

    array = ts.get_hist_data(stocknumber, start=startdata, end=enddata)

    if array is None:
        return
    Date = array.index.tolist()
    Open = array["open"].tolist()
    Close = array["close"].tolist()
    High = array["high"].tolist()
    Low = array["low"].tolist()
    Candlestick = zip(Date, Open, Close, Low, High)
    return Candlestick


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
    # app.run(host='0.0.0.0',port='80')
