# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:09:29 2019

@author: aaaaa
"""
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json

########## 去公開資訊觀測站，把本益比、股價淨值比爬下來 ##########
url = 'http://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_=' + str(time.time())
list_req = requests.get(url)
soup = BeautifulSoup(list_req.content, "html.parser")
getjson=json.loads(soup.text)

########## 因為是表格式，用dataframe處理會比較方便 ##########
stockdf = pd.DataFrame(getjson['data'],columns=["證券代號","證券名稱","殖利率(%)","股利年度","本益比","股價淨值比","財報年/季"])
PBR = pd.to_numeric(stockdf['股價淨值比'], errors='coerce') < 0.7 # 找到股價淨值比小於0.7的股票
EPS = pd.to_numeric(stockdf['本益比'], errors='coerce') < 13 # 找到本益比小於13的股票
candidate= stockdf[(PBR & EPS)] # 綜合以上兩者，選出兩者皆符合的股票

elected='' # 最後可以買的股票放這裡
if len(candidate) > 10 : # 看看這些股票的數量有沒有超過100
    for i in candidate['證券代號']: # 把股票代號丟進去，一個一個茶價格
        url = 'https://tw.stock.yahoo.com/q/q?s=' + i
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getstock= soup.find('b').text
        if float(getstock) > 10: # 如果股價大於10元，就當選
            elected = elected + i + '\n'
else:
    elected='符合的股票小於100，不做操作'

########## 秀出結果 ##########            
if elected != '':# 判斷是不是空直
    print(elected)
else:
    print('沒有股票可以買')
