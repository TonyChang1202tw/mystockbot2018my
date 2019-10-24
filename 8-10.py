# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:55:39 2019

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
start = datetime.datetime.now() - datetime.timedelta(days=365) #先設定要爬的時間
end = datetime.date.today()

# 與yahoo請求
pd.core.common.is_list_like = pd.api.types.is_list_like
yf.pdr_override()

# 取得股票資料
stock = data.get_data_yahoo(userstock+'.TW', start, end)

# 股票MFI圖
ret = pd.DataFrame(talib.MFI(stock['High'].values,stock['Low'].values,stock['Close'].values,stock['Volume'].values.astype(float), timeperiod=14), columns= ['Money Flow Index'])
ret = ret.set_index(stock['Close'].index.values)

### 開始畫圖 ###
ret.plot(color=['#5599FF'], linestyle='dashed')
stock['Close'].plot(secondary_y=True,color='#FF0000')
plt.title("Money_Flow_Index") # 標題設定
plt.show()
