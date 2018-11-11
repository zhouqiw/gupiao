#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import math
import pandas as pd
import numpy as np
import tushare as ts
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# begin_time = '2017-02-01'
# end_time = '2017-11-01'
# code = "000001"
# stock = ts.get_hist_data(code, start=begin_time, end=end_time)
# stock = stock.sort_index(0) # 将数据按照日期排序下。
# stock.to_pickle("stock_data_000001.pickle")
# print("finish save ...")
# 读取股票数据分析。不用每次网络请求数据
stock = pd.read_pickle("stock_data_000001.pickle")
# 5周期、10周期、20周期和60周期
# 周线、半月线、月线和季度线
stock["5d"] = stock["close"].rolling(window=5).mean()  # 周线
stock["10d"] = stock["close"].rolling(window=10).mean()  # 半月线
stock["20d"] = stock["close"].rolling(window=20).mean()  # 月线
stock["60d"] = stock["close"].rolling(window=60).mean()  # 季度线

def kxian():


    #print(stock.head(1))
    #展示股票收盘价格信息

    stock[["close","5d","10d","20d","60d",]].plot(figsize=(20,8), grid=True)
    plt.show()


#计算股票的收益价格
def gu_p():
    stock["return"] = np.log( stock["close"] / stock["close"].shift(1))
    # stock["return_a"] = stock["close"] / stock["close"].shift(1)
    # print(stock[["return","return_a"]].head(15))
    stock[["close","return"]].plot(subplots=True, style='b', figsize=(20,8), grid=True)
    plt.show()

def gp_get_history():
    #计算股票的【收益率的移动历史标准差】
    mov_day = int(len(stock)/20)
    stock["mov_vol"] = stock["return"].rolling(window = mov_day).std()*math.sqrt(mov_day)
    #print(stock["mov_vol"].head(mov_day+1))

    stock[["close","mov_vol","return"]].plot(subplots=True, style='b', figsize=(20,10), grid=True)
    plt.show()

    # print(stock[["mov_vol","return"]].tail(30))
    # print(stock["mov_vol"].tail(5).sum())
    # print(stock["mov_vol"].tail(10).sum())
    # print(stock["mov_vol"].tail(15).sum())
    # print(stock["mov_vol"].describe())


gu_p()
gp_get_history()
