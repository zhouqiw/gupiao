# encoding: utf-8

"""
@author: zhouqi
@software: PyCharm
@file: 1.py
@time: 2018/1/19 下午8:59
"""

# import pandas_datareader.data as web
# china = web.DataReader(name='600848.ss', data_source='yahoo', start='2016-1-1', end='2016-1-31')
# print(china)


import tushare as ts
# histd = ts.get_hist_data(code='600848', start='2016-01-01', end='2016-07-31', ktype='D')
# # histd.sort_index(inplace=True)
#
# tick = ts.get_tick_data(code='600848', date='2016-08-22')
# tick.sort_values('time', inplace=True)
# tick.index = tick['time']
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.dates as mdt
import matplotlib.pylab as plt
import matplotlib.finance as mpf
import tushare as ts

# histd[['ma5', 'ma10', 'ma20']].plot(figsize=(8,5), grid=True, rot=30)

histd = ts.get_hist_data(code='600848', start='2016-01-01', end='2016-07-31', ktype='D',)
print(histd)
# 2, 调整次序到ohlc
collist = list(histd)
collist.insert(2, collist.pop(collist.index('low')))
histd = histd.loc[:, collist]
# 3, 调整DateTime格式到float(网上有类似的转换方法,可能基于不同的版本,在我的环境下没有成功)
histd.reset_index(inplace=True)  # drop the date index
histd['date']= pd.to_datetime(histd['date']) # convert str to date
histd['date'] = mdt.date2num(histd['date'].astype(dt.date))  #convert date to float days
# 4, 转换DataFrame为Numpy.Array(网上有重新构建tuple的方法,我觉得转换成Numpy Array更直接)
hista = np.array(histd)
# 5, 利用hista画出蜡烛图
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(8, 5))
fig.subplots_adjust(bottom=0.2)
mpf.candlestick_ohlc(ax1, hista, width=0.5, colorup='r', colordown='g')
ax1.xaxis_date()
ax1.grid(True)
plt.bar(hista[:,0]-0.25, hista[:, 5], width=0.5)
ax2.grid(True)
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.show()