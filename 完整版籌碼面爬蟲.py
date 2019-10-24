# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:06:06 2019

@author: aaaaa
"""

#繪圖用
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import datetime
from io import StringIO
import pandas as pd
    

# 畫出籌碼面圖
stocknumber='2002'

sumstock=[]
stockdate=[]
for i in range(11,0,-1):
    date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i),'%Y%m%d') #先設定要爬的時間
    r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999') #要爬的網站
    if r.text != '\r\n': #有可能會沒有爬到東西，有可能是六日
        get = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any') # 把交易所的csv資料載下來
        get=get[get['證券代號']==stocknumber] # 找到我們要搜尋的股票
        if len(get) >0:
            get['三大法人買賣超股數'] = get['三大法人買賣超股數'].str.replace(',','').astype(float) # 去掉','這個符號把它轉成數字
            stockdate.append(date)
            sumstock.append(get['三大法人買賣超股數'].values[0])
if len(stockdate) >0:
    ### 開始畫圖 ###
    plt.bar(stockdate, sumstock) 
    plt.xticks(fontsize=10,rotation=90)
    plt.axhline(0, color='c', linewidth=1) # 繪製0的那條線
    plt.title('Institutional Investors', fontsize=20)
    plt.xlabel("Day", fontsize=15)
    plt.ylabel("Quantity", fontsize=15)
    plt.show()
#    plt.savefig('showII.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
