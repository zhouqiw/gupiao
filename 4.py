# encoding: utf-8

"""
@author: zhouqi
@software: PyCharm
@file: 4.py
@time: 2018/10/31 下午10:51
"""
import os
import pandas as pd
import tushare as ts
from factorset.factors import BaseFactor
from factorset.data.OtherData import code_to_symbol, shift_date, market_value
from factorset.data import CSVParser as cp
from factorset.Util.finance import ttmContinues

class EP_TTM(BaseFactor):
    """
    :名称: 过去滚动4个季度（12月）市盈率的倒数
    :计算方法: EP_TTM = 净利润（不含少数股东权益）_TTM /总市值
    :应用: 市盈率越低，代表投资者能够以相对较低价格购入股票。

    """

    def __init__(self, factor_name='EP_TTM', tickers='000016.SH', data_source='', factor_parameters={}, save_dir=None):
        # Initialize super class.
        super(EP_TTM, self).__init__(factor_name=factor_name, tickers=tickers,
                                     factor_parameters=factor_parameters,
                                     data_source=data_source, save_dir=save_dir)

    def prepare_data(self, begin_date, end_date):
        """
        数据预处理
        """

        shifted_begin_date = shift_date(begin_date, 500) # 向前取500个交易日

        # 取利润表中“归属于母公司股东的净利润”项目，项目名称及数字详见FundDict
        inst = cp.concat_fund(self.data_source, self.tickers, 'IS').loc[shifted_begin_date:end_date,['ticker', 40]]
        inst['motherNetProfit'] = inst[40]
        inst.drop(40, axis=1, inplace=True)

        # ttm算法需要“财报发布日”与“财报报告日”两个日期作为参数
        inst['release_date'] = inst.index
        inst['report_date'] = inst.index

        # 净利润ttm
        profitTTM_ls = []
        for ticker in inst['ticker'].unique():
            try:  # 财务数据不足4条会有异常
                reven_df = ttmContinues(inst[inst['ticker'] == ticker], 'motherNetProfit')
                reven_df['ticker'] = ticker
            except:
                continue
            profitTTM_ls.append(reven_df)
        self.profitTTM = pd.concat(profitTTM_ls)

        # 取“OtherData”中总市值数据
        # Tushare的市值数据只有17年6月->now
        df = market_value(self.data_source + '\\other\\otherdata.csv', self.tickers)
        self.mkt_value = df.drop(['price', 'totals'], axis=1)

    def generate_factor(self, trading_day):
        # generate_factor会遍历交易日区间, 即生成每个交易日所有股票的因子值
        earings_df = self.profitTTM[self.profitTTM['datetime'] <= trading_day]
        earings_df = earings_df.sort_values(by=['datetime', 'report_date'], ascending=[False, False])

        # 取最近1期ttm数据
        earings_df = earings_df.groupby('ticker').apply(lambda x: x.head(1))

        # 取当前交易日市值数据
        today_mkt_value = self.mkt_value.loc[trading_day]

        ret_df = earings_df.merge(today_mkt_value, on='ticker', how='inner')
        ret_df['EP_TTM'] = ret_df['motherNetProfit_TTM'] / ret_df['mkt_value']
        return ret_df.set_index('ticker')['EP_TTM']

if __name__ == '__main__':
    from_dt = '2017-07-15'
    to_dt = '2018-04-09'

    # 取沪深300
    hs300 = ts.get_hs300s()
    hs300.code = hs300.code.apply(code_to_symbol)

    EP_TTM = EP_TTM(
        factor_name='EP_TTM',
        factor_parameters={},
        tickers=hs300.code.tolist(),
        save_dir='',
        data_source=os.path.abspath('.'),
    )

    EP_TTM.generate_factor_and_store(from_dt, to_dt)
    print('因子构建完成，并已成功入库!')