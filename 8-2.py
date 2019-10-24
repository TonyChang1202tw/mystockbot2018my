# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:39:06 2019

@author: aaaaa
"""

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data
import fix_yahoo_finance as yf # yahoo專用的拿來拉股票資訊
import datetime
import matplotlib.pyplot as plt # 繪圖專用
import talib #技術分析專用

userstock='2002'
start = datetime.datetime.now() - datetime.timedelta(days=30) #先設定要爬的時間
end = datetime.date.today()

# 與yahoo請求
pd.core.common.is_list_like = pd.api.types.is_list_like
yf.pdr_override()

# 取得股票資料
stock = data.get_data_yahoo(userstock+'.TW', start, end)

# 股票KD圖
ret = pd.DataFrame(list(talib.STOCH(stock['High'].values, stock['Low'].values, stock['Close'].values))).transpose()
ret.columns=['K','D']
ret.index = stock['Close'].index

### 開始畫圖 ###
ret.plot(color=['#5599FF','#66FF66'], linestyle='dashed')

stock['Close'].plot(secondary_y=True,color='#FF0000')
plt.title("KD") # 標題設定
plt.show()
