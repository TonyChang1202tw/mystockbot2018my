# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:08:47 2019

@author: aaaaa
"""


from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

#全台灣所有股票，太多了這邊省略只放三隻
data =['1101.TW', '1102.TW', '1103.TW']

elected='' # 最後可以買的股票放這裡
########## 爬下殖利率、股利 ##########
for i in data:
    url = 'http://invest.wessiorfinance.com/Eps_dividend/get_eps_dividend?Stock=' + i[:4]
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson=json.loads(soup.text)
    stockdf = pd.DataFrame(getjson)
    stockdf=stockdf.drop(8) # 殺掉最後億筆資料，因為最後億筆資料是今年的，有可能今年還沒發放股利，會導至全部都不符合條件
    
    # 現金股利大於0
    dividend_cash = stockdf['dividend_cash'] > 0
    # 平均殖利率大於5
    yield_avg = stockdf['yield_avg'] > 1
    if len(stockdf[(dividend_cash & yield_avg)]) == 8: #等於八是說，八筆資料都要符合，已就是每年都要要符合上述所有條件
        elected = elected + i + '\n'
        
########## 秀出結果 ##########            
if elected != '':# 判斷是不是空直
    print(elected)
else:
    print('沒有股票可以買')
