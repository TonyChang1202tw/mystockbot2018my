# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:08:11 2019

@author: aaaaa
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

elected='' # 最後可以買的股票放這裡
########## 當短期5日線突破20日線 ##########
url = 'https://tw.screener.finance.yahoo.net/screener/ws?PickID=100205&PickCount=1700&f=j'
list_req = requests.get(url)
soup = BeautifulSoup(list_req.content, "html.parser")
getjson1=json.loads(soup.text)

########## 股本大於20億 ##########
url = 'https://tw.screener.finance.yahoo.net/screener/ws?PickID=100538,100539,100540,100541&PickCount=20&f=j&366'
list_req = requests.get(url)
soup = BeautifulSoup(list_req.content, "html.parser")
getjson2=json.loads(soup.text)

for i in getjson1['items']:
    if i['symid'] in str(getjson2['items']):
########## 週均量大於 1000 張 ##########   
        url = 'https://tw.stock.yahoo.com/q/q?s=' + i['symid']
        getjson3=pd.read_html(url,encoding='big5',header=0)
        if getjson3[5]['張數'].values[0] >1000 :
            elected = elected + i['symid'] + '\n'
            
########## 秀出結果 ##########            
if elected != '':# 判斷是不是空直
    print(elected)
else:
    print('沒有股票可以買')
