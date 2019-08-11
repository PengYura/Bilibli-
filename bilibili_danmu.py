#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 07:52:39 2019

@author: yura
"""
import requests
import re
import datetime
import pandas as pd
import random
import time



video_time=[]
abstime=[]
userid=[]
comment_content=[]

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

#视频发布时间～当日
search_time=dateRange("2019-07-26", "2019-08-09")

headers = {
        'Host': 'api.bilibili.com',
		'Connection': 'keep-alive',
		'Content-Type': 'text/xml',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': '',
		'Origin': 'https://www.bilibili.com',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
        }

#cookie用火狐浏览器找，以字典形式写入
cookie={           
#        '_dfcaptcha':'2dd6f170a70dd9d39711013946907de0',
        'bili_jct':'bili_jct5bbff2af91bd6d6c219d1fafa51ce179',
        'buvid3':'4136E3A9-5B93-47FD-ACB8-6681EB0EF439155803infoc',
        'CURRENT_FNVAL':'16',
        'DedeUserID':'293928856',
        'DedeUserID__ckMd5':'6dc937ced82650a6',
        'LIVE_BUVID':'AUTO6915654009867897',
#        'rpdid':'owolosliwxdossokkkoqw',
        'SESSDATA':'72b81477%2C1567992983%2Cbd6cb481',
        'sid':'i2a1khkk',
        'stardustvideo':'1',
        }

url='https://api.bilibili.com/x/v2/dm/history?type=1&oid=105743914&date={}'

for search_data in search_time:
    print('正在爬取{}的弹幕'.format(search_data))
    full_url=url.format(search_data)
    res=requests.get(full_url,headers=headers,timeout=10,cookies=cookie)
    res.encoding='utf-8'  
    data_number=re.findall('d p="(.*?)">',res.text,re.S)
    data_text=re.findall('">(.*?)</d>',res.text,re.S)
    
    comment_content.extend(data_text)
    for each_numbers in data_number:
        each_numbers=each_numbers.split(',')
        video_time.append(each_numbers[0])           
        abstime.append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(each_numbers[4]))))      
        userid.append(each_numbers[6])
    time.sleep(random.random()*3)


print(len(comment_content))
print('爬取完成')
result={'用户id':userid,'评论时间':abstime,'视频位置(s)':video_time,'弹幕内容':comment_content}

results=pd.DataFrame(result)
final= results.drop_duplicates()
final.info()
final.to_excel('B站弹幕（哪吒）.xlsx')
