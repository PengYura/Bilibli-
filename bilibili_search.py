#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 21:59:33 2019

@author: yura
"""
from bs4 import BeautifulSoup
import requests
import warnings
import re
from datetime import datetime
import json
import pandas as pd
import random
import time
import datetime
from multiprocessing import Pool


headers = {
    'User-Agent': ''
    'Referer':'https://www.bilibili.com/',
    'Connection':'keep-alive'}
    
cookies={'cookie':''}

def get_bilibili_oubing(url):
    avid=[]
    video_type=[]
    watch_count=[]
    comment_count=[]
    up_time=[]
    up_name=[]
    title=[]
    duration=[]
    
    print('正在爬取{}'.format(url))
    time.sleep(random.random()+2)
    res=requests.get(url,headers=headers,cookies=cookies,timeout=30)
    
    soup=BeautifulSoup(res.text,'html.parser')
    
    
    #avi号码
    avids=soup.select('.avid')
    
    #视频类型
    videotypes=soup.find_all('span',class_="type hide")

    #观看数
    watch_counts=soup.find_all('span',title="观看")
    
    #弹幕
    comment_counts=soup.find_all('span',title="弹幕")
    
    #上传时间
    up_times=soup.find_all('span',title="上传时间")
    
    #up主
    up_names=soup.find_all('span',title="up主")

    #title
    titles=soup.find_all('a',class_="title")
    #时长
    durations=soup.find_all('span',class_='so-imgTag_rb')
    
    for i in range(20):
        avid.append(avids[i].text)
        video_type.append(videotypes[i].text)
        watch_count.append(watch_counts[i].text.strip())
        comment_count.append(comment_counts[i].text.strip())
        up_time.append(up_times[i].text.strip())
        up_name.append(up_names[i].text)
        title.append(titles[i].text)
        duration.append(durations[i].text)
        
    result={'视频id':avid,'视频类型':video_type,'观看次数':watch_count,'弹幕数量':comment_count,'上传时间':up_time,'up主':up_name,'标题':title,'时长':duration}

    results=pd.DataFrame(result)
    return results

 
if __name__=='__main__': 
    url_original='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=totalrank&duration=0&tids_1=0&page={}'
    url_click='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=click&duration=0&tids_1=0&page={}'
    url_favorite='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=stow&duration=0&tids_1=0&page={}'
    url_bullet='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=dm&duration=0&tids_1=0&page={}'
    url_new='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=pubdate&duration=0&tids_1=0&page={}'
    all_url=[url_bullet,url_click,url_favorite,url_new,url_original]

    info_df=pd.DataFrame(columns = ['视频id','视频类型','观看次数','弹幕数量','上传时间','up主','标题','时长']) 
    for i in range(50):
        for url in all_url:
            full_url=url.format(i+1)
            info_df=pd.concat([info_df,get_bilibili_oubing(full_url)],ignore_index=True)
      
    print('爬取完成！')
    #去重
    info_df=info_df.drop_duplicates(subset=['视频id'])
    info_df.info()
    info_df.to_excel('哪吒.xlsx')
        