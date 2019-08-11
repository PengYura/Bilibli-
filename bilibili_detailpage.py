#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:58:24 2019

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



url='https://api.bilibili.com/x/web-interface/view?aid={}'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer':'https://www.bilibili.com/',
    'Connection':'keep-alive'}
    
cookies={'cookie':'LIVE_BUVID=AUTO6415404632769145; sid=7lzefkl6; stardustvideo=1; CURRENT_FNVAL=16; rpdid=kwmqmilswxdospwpxkkpw; fts=1540466261; im_notify_type_293928856=0; CURRENT_QUALITY=64; buvid3=D1539899-8626-4E86-8D7B-B4A84FC4A29540762infoc; _uuid=79056333-ED23-6F44-690F-1296084A1AAE80543infoc; gr_user_id=32dbb555-8c7f-4e11-beb9-e3fba8a10724; grwng_uid=03b8da29-386e-40d0-b6ea-25dbc283dae5; UM_distinctid=16b8be59fb13bc-094e320148f138-37617e02-13c680-16b8be59fb282c; DedeUserID=293928856; DedeUserID__ckMd5=6dc937ced82650a6; SESSDATA=b7d13f3a%2C1567607524%2C4811bc81; bili_jct=6b3e565d30678a47c908e7a03254318f; _uuid=01B131EB-D429-CA2D-8D86-6B5CD9EA123061556infoc; bsource=seo_baidu'}

k=0
def get_bilibili_detail(id):
    global k
    k=k+1
    print(k)
    full_url=url.format(id[2:])
    try:
        res=requests.get(full_url,headers=headers,cookies=cookies,timeout=30)
        time.sleep(random.random()+1)
        print('正在爬取{}'.format(id))
        
        content=json.loads(res.text,encoding='utf-8')
        test=content['data']
        
    except:
        print('error')
        info={'视频id':id,'最新弹幕数量':'','金币数量':'','不喜欢':'','收藏':'','最高排名':'','点赞数':'','目前排名':'','回复数':'','分享数':'','观看数':''}
        return info
    else:
 
        danmu=content['data']['stat']['danmaku']
        coin=content['data']['stat']['coin']
        dislike=content['data']['stat']['dislike']
        favorite=content['data']['stat']['favorite']
        his_rank=content['data']['stat']['his_rank']
        like=content['data']['stat']['like']
        now_rank=content['data']['stat']['now_rank']
        reply=content['data']['stat']['reply']
        share=content['data']['stat']['share']
        view=content['data']['stat']['view']
    info={'视频id':id,'最新弹幕数量':danmu,'金币数量':coin,'不喜欢':dislike,'收藏':favorite,'最高排名':his_rank,'点赞数':like,'目前排名':now_rank,'回复数':reply,'分享数':share,'观看数':view}
    
    return info

if __name__=='__main__': 
    df=pd.read_excel('哪吒.xlsx')
    avids=df['视频id']
    detail_lists=[]
    for id in avids:
        detail_lists.append(get_bilibili_detail(id))

    reshape_df=pd.DataFrame(detail_lists) 
    final_df=pd.merge(df,reshape_df,how='inner',on='视频id')
    final_df.to_excel('藕饼cp详情new.xlsx')
    final_df.info()
#    final_df.duplicated(['视频id'])
#    reshape_df.to_excel('藕饼cp.xlsx')
        
