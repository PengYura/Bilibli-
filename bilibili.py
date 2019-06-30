#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 07:52:39 2019

@author: yura
"""
import requests
import re
from datetime import datetime
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
search_time=dateRange("2016-01-10", "2019-06-25")

headers = {
        'Host': 'api.bilibili.com',
		'Connection': 'keep-alive',
		'Content-Type': 'text/xml',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': '',
		'Origin': 'https://www.bilibili.com',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
#		'Cookie': 'finger=edc6ecda; LIVE_BUVID=AUTO1415378023816310; stardustvideo=1; CURRENT_FNVAL=8; buvid3=0D8F3D74-987D-442D-99CF-42BC9A967709149017infoc; rpdid=olwimklsiidoskmqwipww; fts=1537803390'
        }
#cookie用火狐浏览器找，以字典形式写入
cookie={           
#        '_dfcaptcha':'2dd6f170a70dd9d39711013946907de0',
#        'bili_jct':'9feece81d443f00759b45952bf66dfff',
#        'buvid3':'DDCE08BC-0FFE-4E4E-8DCF-9C8EB7B2DD3752143infoc',
#        'CURRENT_FNVAL':'16',
#        'DedeUserID':'293928856',
#        'DedeUserID__ckMd5':'6dc937ced82650a6',
#        'LIVE_BUVID':'AUTO7815513331706031',
#        'rpdid':'owolosliwxdossokkkoqw',
#        'SESSDATA':'7e38d733,1564033647,804c5461',
#        'sid':'	9zyorvhg',
#        'stardustvideo':'1',
        }

url='https://api.bilibili.com/x/v2/dm/history?type=1&oid=5627945&date={}'

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
final.to_excel('B站弹幕（天鹅臂）最后.xlsx')
