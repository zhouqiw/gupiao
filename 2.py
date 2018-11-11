# encoding: utf-8

"""
@author: zhouqi
@software: PyCharm
@file: 2.py
@time: 2018/1/21 上午11:43
"""

import tushare as ts

df = ts.get_hist_data('000875')
#直接保存
df.to_csv('000875.csv')

#选择保存
df.to_csv('000875.csv',columns=['open','high','low','close'])
