#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import requests
import json
from jsonpath import jsonpath
from datetime import datetime
import jmespath


# # 基金總攬

# In[2]:


alljson=[]
for offset in range(2):
    url = f'https://fund.api.cnyes.com/fund/api/v2/search/fund?order=priceDate&sort=desc&page={offset+1}&institutional=0&forSale=1&isShowTag=1&fundGroup=G1&classCurrency=TWD&categoryAbbr=C46&onshore=1&fields=categoryAbbr,change,changePercent,classCurrencyLocal,cnyesId,displayNameLocal,displayNameLocalWithKwd,forSale,forSale,inceptionDate,investmentArea,lastUpdate,nav,prevPrice,priceDate,return1Month'
    res = requests.get(url)
    rejson = json.loads(res.text)
    for time in range(len(rejson['items']['data'])):
        alljson.append(rejson['items']['data'][time])  


# In[3]:


df = pd.DataFrame(alljson).drop(['fundTags', 'portfolio_errors', 'displayNameLocalWithKwd', 'forSale'], axis=1).rename(columns={'cnyesId':'基金ID','nav':'最新淨值','change':'漲跌(%)','investmentArea':'投資地區','categoryAbbr':'基金組別','displayNameLocal':'基金名稱','classCurrencyLocal':'幣別','return1Month':'一月績效(%)'})
df['priceDate']=df['priceDate'].apply(lambda x:datetime.fromtimestamp(x))
df['inceptionDate']=df['inceptionDate'].apply(lambda x:datetime.fromtimestamp(x))
df['lastUpdate']=df['lastUpdate'].apply(lambda x:datetime.fromtimestamp(x))
df.to_csv("data.csv",index=False,encoding="utf-8-sig")


# In[4]:


df


# # 整體績效

# In[5]:


alljson3=[]
for offset2 in range(2):
    url = f'https://fund.api.cnyes.com/fund/api/v2/search/fund?order=priceDate&sort=desc&page={offset2+1}&institutional=0&forSale=1&isShowTag=1&classCurrency=TWD&categoryAbbr=C46&onshore=1&fields=accReturn3Year,accReturn5Year,cnyesId,displayNameLocal,forSale,return1Month,return1Week,return1Year,return3Month,return6Month,returnYTD'
    res = requests.get(url)
    rejson = json.loads(res.text)
    for time in range(len(rejson['items']['data'])):
        alljson3.append(rejson['items']['data'][time])  
    print(alljson3)
    
    
    


# In[11]:


df3 = pd.DataFrame(alljson3)
df3 = pd.DataFrame(alljson3).drop(['displayNameLocalWithKwd', 'fundTags', 'portfolio_errors', 'forSale'], axis=1).rename(columns={'return1Week':'一周','cnyesId':'基金ID','return3Month':'三月','displayNameLocal':'基金名稱','return6Month':'六月','return1Month':'一月','return1Year':'一年','returnYTD':'今年以來','accReturn3Year':'三年','accReturn5Year':'五年'})
df3


# # 每日淨值

# In[7]:


alljson1=[]
for offset1 in range(20):
    url=f'https://fund.api.cnyes.com/fund/api/v1/funds/A36004/nav?format=table&page={offset1+1}'
    res = requests.get(url)
    rejson = json.loads(res.text)
    for time in range(len(rejson['items']['data'])):
        alljson1.append(rejson['items']['data'][time])  
    print(alljson1)
    
    


# In[8]:


df1 = pd.DataFrame(alljson1)
df1 = pd.DataFrame(alljson1).rename(columns={'nav':'淨值','nav':'最新淨值','change':'漲跌(%)','changePercent':'漲跌幅'})
df1['tradeDate']=df1['tradeDate'].apply(lambda x:datetime.fromtimestamp(x))
df1


# # 績效走勢

# In[3]:


alljson2=[]

url = 'https://fund.api.cnyes.com/fund/api/v1/funds/A36004/history/performance?by=w&startAt=1460476800'
res = requests.get(url)
rejson = json.loads(res.text)
a=jmespath.search('items.{"每日績效":performance,"日期":tradeDate}',rejson)
     
        
print(a)
    
    
    


# In[4]:


df2 = pd.DataFrame(a)
df2['日期']=df2['日期'].apply(lambda x:datetime.fromtimestamp(x))
df2


# In[ ]:




