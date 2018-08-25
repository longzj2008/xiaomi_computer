#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time,json
from selenium import webdriver
import pandas as pd
from numpy import nan as NaN
from bs4 import BeautifulSoup
import re

#获取比赛的各种网页id，以及初盘信息
def fun_get_ID_name_init(html_soup):
    ##001########获取ID和名字##############################################################################
    ID_links = html_soup.select('#diary_info > table > tbody > tr > td > a')

    ls_game_id = []  # 本场比赛的ID
    ls_league_id = []
    ls_zd_id = []
    ls_kd_id = []
    # 获取名字
    ls_league_name = []
    ls_zd_name = []
    ls_kd_name = []
    # 初盘数据
    ls_init_rangqiu = []
    ls_init_daxiao = []
    ls_init_jiaoqiu = []
    # 获取相关ID，与名字
    num = 0
    for row in ID_links:
        # /league/198 联赛ID
        if num % 6 == 0:
            id = row.get('href').split('/')[-1]
            ls_league_id.append(id)
            name = row.text.strip()
            ls_league_name.append(name)
        # /team/1391 主队ID
        if num % 6 == 1:
            id = row.get('href').split('/')[-1]
            ls_zd_id.append(id)
            name = row.text.strip()
            ls_zd_name.append(name)
        # /team/1401 客队ID
        if num % 6 == 2:
            id = row.get('href').split('/')[-1]
            ls_kd_id.append(id)
            name = row.text.strip()
            ls_kd_name.append(name)
        # /race_sp/490576,获取本场比赛ID
        if num % 6 == 3:
            id = row.get('href').split('/')[-1]
            ls_game_id.append(id)
            name = row.text.strip().split('/')
            try:
                ls_init_rangqiu.append(name[0].strip())
            except:
                ls_init_rangqiu.append(NaN)
            try:
                ls_init_daxiao.append(name[1].strip())
            except:
                ls_init_daxiao.append(NaN)
            try:
                init_jiaoqiu = name[2].strip()
                if init_jiaoqiu == '-':
                    ls_init_jiaoqiu.append(NaN)
                else:
                    ls_init_jiaoqiu.append(init_jiaoqiu)
            except:
                ls_init_jiaoqiu.append(NaN)
        num += 1

    # ##以下代码用于测试
    #     if num==6:
    #         break
    # print(ls_league_id,ls_league_name,ls_zd_id,ls_zd_name,ls_kd_id,ls_kd_name,ls_game_id,ls_init_rangqiu,ls_init_daxiao,
    #       ls_init_jiaoqiu)

    dic={'本场比赛ID':ls_game_id,
         '联赛名称':ls_league_name,'联赛ID':ls_league_id,
         '主_名字':ls_zd_name,'主_ID':ls_zd_id,'客_名字':ls_kd_name,'客_ID':ls_kd_id,
         '初盘_让球':ls_init_rangqiu,'初盘_大小':ls_init_daxiao,'初盘_角球':ls_init_jiaoqiu}
    return(dic)
#获取比赛的红黄牌信息，及球队排名
def fun_get_Card_Pm(html_soup):
    ##002########获取:红，黄牌和联赛排名##############################################################################
    zhudui_cards = html_soup.select('#diary_info > table > tbody > tr > td.text-right.BR0')
    kedui_cards = html_soup.select('#diary_info > table > tbody > tr > td.text-left')
    ls_zd_yc = []
    ls_zd_rc = []
    ls_zd_pm = []
    ls_kd_yc = []
    ls_kd_rc = []
    ls_kd_pm = []
    for card in zhudui_cards:
        # 获取黄牌数量
        try:
            yc = card.find(attrs="yellowCard")
            yc_num = yc.text
        except:
            yc_num = '0'
        ls_zd_yc.append(eval(yc_num))
        # 获取红牌数量
        try:
            rc = card.find(attrs="redCard")
            rc_num = rc.text
        except:
            rc_num = '0'
        ls_zd_rc.append(eval(rc_num))
        # 获取联赛排名
        try:
            pm = card.find(attrs="leagueRank")
            pm_num = pm.text.replace('[', '').replace(']', '')
        except:
            pm_num = '0'
        ls_zd_pm.append(eval(pm_num))
    for card in kedui_cards:
        # 获取黄牌数量
        try:
            yc = card.find(attrs="yellowCard")
            yc_num = yc.text
        except:
            yc_num = '0'
        ls_kd_yc.append(eval(yc_num))
        # 获取红牌数量
        try:
            rc = card.find(attrs="redCard")
            rc_num = rc.text
        except:
            rc_num = '0'
        ls_kd_rc.append(eval(rc_num))
        # 获取联赛排名
        try:
            pm = card.find(attrs="leagueRank")
            pm_num = pm.text.replace('[', '').replace(']', '')
        except:
            pm_num = '0'
        ls_kd_pm.append(eval(pm_num))
    dic={'主_黄牌':ls_zd_yc,'主_红牌':ls_zd_rc,'主_排名':ls_zd_pm,
         '客_黄牌':ls_kd_yc,'客_红牌':ls_kd_rc,'客_排名':ls_kd_pm}
    return (dic)

#01下面3个为获取 比分，获取比分时间，把时间存到一个字符串中
def _fun_get_goals_corners_number_2(html_soup):
    ##003########获取:比分，角球比分##############################################################################
    scores_final_half = html_soup.select('#diary_info > table > tbody > tr > td.text-center.red-color')
    jiaoqiu_final_half = html_soup.select('#diary_info > table > tbody > tr > td.text-center.blue-color')
    ls_zd_score_final = []
    ls_kd_score_final = []
    ls_zd_score_half = []
    ls_kd_score_half = []
    ls_zd_jiaoqiu_final = []
    ls_zd_jiaoqiu_half = []
    ls_kd_jiaoqiu_final = []
    ls_kd_jiaoqiu_half = []
    i = 0
    for score in scores_final_half:
        fen = score.text.split(':')
        if i % 2 == 0:
            ls_zd_score_final.append(fen[0].strip())
            ls_kd_score_final.append(fen[1].strip())
        else:
            ls_zd_score_half.append(fen[0].strip())
            ls_kd_score_half.append(fen[1].strip())
        i += 1
    # 测试用
    #     if i==4:
    #         break
    # print(ls_zd_score_final,ls_kd_score_final,ls_zd_score_half,ls_kd_score_half)
    # 04获取主客队上下半场角球比分
    i = 0
    for score in jiaoqiu_final_half:
        fen = score.text.split(':')
        if i % 2 == 1:
            ls_zd_jiaoqiu_final.append(fen[0].strip())
            ls_kd_jiaoqiu_final.append(fen[1].strip())
        else:
            ls_zd_jiaoqiu_half.append(fen[0].strip())
            ls_kd_jiaoqiu_half.append(fen[1].strip())
        i += 1
    # #测试用
    #     if i==2:
    #         break
    # print(ls_zd_jiaoqiu_final,ls_kd_jiaoqiu_final,ls_zd_jiaoqiu_half,ls_kd_jiaoqiu_half)
    dic={'主_半_比分':ls_zd_score_half,'客_半_比分':ls_kd_score_half,
         '主_全_比分':ls_zd_score_final,'客_全_比分':ls_kd_score_final,
         '主_半_角球':ls_zd_jiaoqiu_half,'客_半_角球':ls_kd_jiaoqiu_half,
         '主_全_角球':ls_zd_jiaoqiu_final,'客_全_角球':ls_kd_jiaoqiu_final,}
    # print(dic)
    return (dic)

def _fun_get_goals_couners_times_2(html_soup):  #获取比赛初盘和ID

    Corners=html_soup.select('#race_timeLine > span.timeLineCorner')
    Goals=html_soup.select('#race_timeLine > span.timeLineGoal')
    ls_zd_corners_times=[]
    ls_kd_corners_times=[]
    ls_zd_goals_times=[]
    ls_kd_goals_times=[]
    num=0
    for i in Corners:
        #'src':"/assets/images/event/timeline-corner-g-7.png"    客队角球的图
        #'src':"/assets/images/event/timeline-corner-h-7.png"    主队角球的图
        # print(i)
        m=i.find(attrs={'src':"/assets/images/event/timeline-corner-g-7.png"})
        if m:
            # print('客队角球{}'.format(i.get('title')))
            time=i.get('title').split('-')[0].strip()
            ls_kd_corners_times.append(time)
        else:
            # print('主队角球{}'.format(i.get('title')))
            time = i.get('title').split('-')[0].strip()
            ls_zd_corners_times.append(time)
        num+=1
    # print(ls_zd_jiaoqiu_times,ls_kd_jiaoqiu_times)

    num=0
    for i in Goals:
        # 'src':"/assets/images/event/gg.png"     客队进球的图
        #"/assets/images/event/gw.png"  主队乌龙球 图标，代表客队进球
        #<img src="/assets/images/event/gp.png" class="" alt="点球">  客队点球进球
        #<img src="/assets/images/event/gmp.png" class="" alt="点球射失"> 客队射失点球
        #<img src="/assets/images/event/ggc.png" class="" alt="ggc"> 客队进球取消

        #    'src':"/assets/images/event/hg.png"     主队进球的图
        # "/assets/images/event/hw.png"  客队乌龙球 图标，代表主队进球
        #<img src="/assets/images/event/hmp.png" class="" alt="点球射失"> 主队射失点球
        #<img src="/assets/images/event/hp.png" class="" alt="点球"> 主队点球成功
        #<img src="/assets/images/event/hgc.png" class="" alt="hgc"> 主队进球取消
        # print(i)
        m = i.find(attrs={'src':"/assets/images/event/gg.png"}) #射门进球
        n = i.find(attrs={'src':"/assets/images/event/gw.png"}) #乌龙进球
        q =i.find(attrs={'src':"/assets/images/event/gp.png"})  #点球进球

        r = i.find(attrs={'src':"/assets/images/event/hg.png"})
        s = i.find(attrs={'src':"/assets/images/event/hw.png"})
        t =i.find(attrs={'src':"/assets/images/event/hp.png"})

        if m or n or q:
            # print('客队进球{}'.format(i.get('title')))
            time = i.get('title').split('-')[0].strip()
            ls_kd_goals_times.append(time)


        elif r or s or t:
            # print('主队进球{}'.format(i.get('title')))
            time = i.get('title').split('-')[0].strip()
            ls_zd_goals_times.append(time)
        num += 1

    dic={'主_全_进球时间':ls_zd_goals_times,'客_全_进球时间':ls_kd_goals_times,
         '主_全_角球时间':ls_zd_corners_times,'客_全_角球时间':ls_kd_corners_times}
    # print(dic)
    return (dic)

def _fun_get_goals_couners_num_time_1(html_soup):  #获取比赛初盘和ID
    dic_num=_fun_get_goals_corners_number_2(html_soup)
    dic_times=_fun_get_goals_couners_times_2(html_soup)

    #结果
    ls_zd_goals_time=[]
    ls_zd_corners_time = []
    ls_kd_goals_time = []
    ls_kd_corners_time = []
    #存放数量
    ls_zd_goals_num=map(int,dic_num['主_全_比分'])
    ls_zd_corners_num =map(int,dic_num['主_全_角球'])
    ls_kd_goals_num= map(int,dic_num['客_全_比分'])
    ls_kd_corners_num = map(int,dic_num['客_全_角球'])
    #存放时间
    ls_zd_goals_times=dic_times['主_全_进球时间']
    ls_zd_corners_times = dic_times['主_全_角球时间']
    ls_kd_goals_times = dic_times['客_全_进球时间']
    ls_kd_corners_times = dic_times['客_全_角球时间']


    for num in ls_zd_goals_num:
        ls = []
        for i in range(num):
            if len(ls_zd_goals_times)==0:
                ls.append('150')
            else:
                ls.append(ls_zd_goals_times.pop(0))
        ls_zd_goals_time.append(','.join(ls))
    #用于测试
    # print(len(dic_num['主_全_比分']))
    # print(len(ls_zd_goals_time))
    # print(ls_zd_goals_time)

    for num in ls_kd_goals_num:
        ls = []
        for i in range(num):
            if len(ls_kd_goals_times)==0:
                ls.append('150')
            else:
                ls.append(ls_kd_goals_times.pop(0))
        ls_kd_goals_time.append(','.join(ls))
    #用于测试
    # print(len(dic_num['主_全_比分']))
    # print(len(ls_kd_goals_time))
    # print(ls_kd_goals_time)

    for num in ls_zd_corners_num:
        ls = []
        for i in range(num):
            if len(ls_zd_corners_times)==0:
                ls.append('150')
            else:
                ls.append(ls_zd_corners_times.pop(0))
        ls_zd_corners_time.append(','.join(ls))

    for num in ls_kd_corners_num:
        ls = []
        for i in range(num):
            if len(ls_kd_corners_times)==0:
                ls.append('150')
            else:
                ls.append(ls_kd_corners_times.pop(0))
        ls_kd_corners_time.append(','.join(ls))

    dic_time={'主_全_进球时间':ls_zd_goals_time,'客_全_进球时间':ls_kd_goals_time,
         '主_全_角球时间':ls_zd_corners_time,'客_全_角球时间':ls_kd_corners_time}
    # print(len(ls_kd_corners_time),len(ls_zd_corners_time),len(ls_kd_goals_time),len(ls_zd_goals_time))
    #字典的合并操作
    dic=dict()
    dic.update(dic_num)
    dic.update(dic_time)
    return (dic)

    #把进球时间分开

#01下面4个为把时间字符串分割 时间列表的函数，进球分成10个组，角球分成20个组
def zd_goal_time(dic_input):
    ls_zd_goal_time=dic_input['主_全_进球时间']
    ls_zd_goal_1_time=[]
    ls_zd_goal_2_time=[]
    ls_zd_goal_3_time=[]
    ls_zd_goal_4_time=[]
    ls_zd_goal_5_time=[]
    ls_zd_goal_6_time=[]
    ls_zd_goal_7_time=[]
    ls_zd_goal_8_time=[]
    ls_zd_goal_9_time=[]
    ls_zd_goal_10_time=[]
    for time in ls_zd_goal_time:

        ls =[]

        try:
            ls =time.replace('\'' ,'').split(',')
            ls = list(map(eval, ls))    #把列表中元素变为整形，有+号的计算
            ls.sort()               #列表从小到大排序
        except:
            ls=[]
        lenth=len(ls)
        num_goals=10
        for i in range(num_goals-lenth):
            ls.append('150')        #设定没有进球的时间为150，代表没有进球

        ls_zd_goal_1_time .append(ls[0])
        ls_zd_goal_2_time .append(ls[1])
        ls_zd_goal_3_time .append(ls[2])
        ls_zd_goal_4_time .append(ls[3])
        ls_zd_goal_5_time .append(ls[4])
        ls_zd_goal_6_time .append(ls[5])
        ls_zd_goal_7_time .append(ls[6])
        ls_zd_goal_8_time .append(ls[7])
        ls_zd_goal_9_time .append(ls[8])
        ls_zd_goal_10_time .append(ls[9])
    dic={'主_进1_时间':ls_zd_goal_1_time,
         '主_进2_时间': ls_zd_goal_2_time,
         '主_进3_时间': ls_zd_goal_3_time,
         '主_进4_时间': ls_zd_goal_4_time,
         '主_进5_时间': ls_zd_goal_5_time,
         '主_进6_时间': ls_zd_goal_6_time,
         '主_进7_时间': ls_zd_goal_7_time,
         '主_进8_时间': ls_zd_goal_8_time,
         '主_进9_时间': ls_zd_goal_9_time,
         '主_进10_时间': ls_zd_goal_10_time,
         }
    return (dic)

def kd_goal_time(dic_input):
    ls_kd_goal_time=dic_input['客_全_进球时间']
    ls_kd_goal_1_time=[]
    ls_kd_goal_2_time=[]
    ls_kd_goal_3_time=[]
    ls_kd_goal_4_time=[]
    ls_kd_goal_5_time=[]
    ls_kd_goal_6_time=[]
    ls_kd_goal_7_time=[]
    ls_kd_goal_8_time=[]
    ls_kd_goal_9_time=[]
    ls_kd_goal_10_time=[]
    for time in ls_kd_goal_time:
        ls =[]
        try:
            ls =time.replace('\'' ,'').split(',')
            ls = list(map(eval, ls))    #把列表中元素变为整形，有+号的计算
            ls.sort()               #列表从小到大排序
        except:
            ls=[]
        lenth=len(ls)
        num_goals=10
        for i in range(num_goals-lenth):
            ls.append('150')        #设定没有进球的时间为150，代表没有进球

        ls_kd_goal_1_time .append(ls[0])
        ls_kd_goal_2_time .append(ls[1])
        ls_kd_goal_3_time .append(ls[2])
        ls_kd_goal_4_time .append(ls[3])
        ls_kd_goal_5_time .append(ls[4])
        ls_kd_goal_6_time .append(ls[5])
        ls_kd_goal_7_time .append(ls[6])
        ls_kd_goal_8_time .append(ls[7])
        ls_kd_goal_9_time .append(ls[8])
        ls_kd_goal_10_time .append(ls[9])
    dic={'客_进1_时间':ls_kd_goal_1_time,
         '客_进2_时间': ls_kd_goal_2_time,
         '客_进3_时间': ls_kd_goal_3_time,
         '客_进4_时间': ls_kd_goal_4_time,
         '客_进5_时间': ls_kd_goal_5_time,
         '客_进6_时间': ls_kd_goal_6_time,
         '客_进7_时间': ls_kd_goal_7_time,
         '客_进8_时间': ls_kd_goal_8_time,
         '客_进9_时间': ls_kd_goal_9_time,
         '客_进10_时间': ls_kd_goal_10_time,
         }
    return (dic)

def zd_corner_time(dic_input):
    ls_zd_corner_time=dic_input['主_全_角球时间']
    ls_zd_corner_1_time=[]
    ls_zd_corner_2_time=[]
    ls_zd_corner_3_time=[]
    ls_zd_corner_4_time=[]
    ls_zd_corner_5_time=[]
    ls_zd_corner_6_time=[]
    ls_zd_corner_7_time=[]
    ls_zd_corner_8_time=[]
    ls_zd_corner_9_time=[]
    ls_zd_corner_10_time=[]
    ls_zd_corner_11_time=[]
    ls_zd_corner_12_time=[]
    ls_zd_corner_13_time=[]
    ls_zd_corner_14_time=[]
    ls_zd_corner_15_time=[]
    ls_zd_corner_16_time=[]
    ls_zd_corner_17_time=[]
    ls_zd_corner_18_time=[]
    ls_zd_corner_19_time=[]
    ls_zd_corner_20_time = []
    for time in ls_zd_corner_time:
        ls =[]

        try:
            ls =time.replace('\'' ,'').split(',')
            ls = list(map(eval, ls))    #把列表中元素变为整形，有+号的计算
            ls.sort()               #列表从小到大排序
        except:
            ls=[]
        lenth=len(ls)
        num_goals=20
        for i in range(num_goals-lenth):
            ls.append('150')        #设定没有进球的时间为150，代表没有进球

        ls_zd_corner_1_time .append(ls[0])
        ls_zd_corner_2_time .append(ls[1])
        ls_zd_corner_3_time .append(ls[2])
        ls_zd_corner_4_time .append(ls[3])
        ls_zd_corner_5_time .append(ls[4])
        ls_zd_corner_6_time .append(ls[5])
        ls_zd_corner_7_time .append(ls[6])
        ls_zd_corner_8_time .append(ls[7])
        ls_zd_corner_9_time .append(ls[8])
        ls_zd_corner_10_time .append(ls[9])
        ls_zd_corner_11_time.append(ls[10])
        ls_zd_corner_12_time.append(ls[11])
        ls_zd_corner_13_time.append(ls[12])
        ls_zd_corner_14_time.append(ls[13])
        ls_zd_corner_15_time.append(ls[14])
        ls_zd_corner_16_time.append(ls[15])
        ls_zd_corner_17_time.append(ls[16])
        ls_zd_corner_18_time.append(ls[17])
        ls_zd_corner_19_time.append(ls[18])
        ls_zd_corner_20_time.append(ls[19])
    dic={'主_角1_时间':ls_zd_corner_1_time,
         '主_角2_时间': ls_zd_corner_2_time,
         '主_角3_时间': ls_zd_corner_3_time,
         '主_角4_时间': ls_zd_corner_4_time,
         '主_角5_时间': ls_zd_corner_5_time,
         '主_角6_时间': ls_zd_corner_6_time,
         '主_角7_时间': ls_zd_corner_7_time,
         '主_角8_时间': ls_zd_corner_8_time,
         '主_角9_时间': ls_zd_corner_9_time,
         '主_角10_时间': ls_zd_corner_10_time,
         '主_角11_时间': ls_zd_corner_11_time,
         '主_角12_时间': ls_zd_corner_12_time,
         '主_角13_时间': ls_zd_corner_13_time,
         '主_角14_时间': ls_zd_corner_14_time,
         '主_角15_时间': ls_zd_corner_15_time,
         '主_角16_时间': ls_zd_corner_16_time,
         '主_角17_时间': ls_zd_corner_17_time,
         '主_角18_时间': ls_zd_corner_18_time,
         '主_角19_时间': ls_zd_corner_19_time,
         '主_角20_时间': ls_zd_corner_20_time,
         }
    return (dic)

def kd_corner_time(dic_input):
    ls_kd_corner_time=dic_input['客_全_角球时间']
    ls_kd_corner_1_time=[]
    ls_kd_corner_2_time=[]
    ls_kd_corner_3_time=[]
    ls_kd_corner_4_time=[]
    ls_kd_corner_5_time=[]
    ls_kd_corner_6_time=[]
    ls_kd_corner_7_time=[]
    ls_kd_corner_8_time=[]
    ls_kd_corner_9_time=[]
    ls_kd_corner_10_time=[]
    ls_kd_corner_11_time=[]
    ls_kd_corner_12_time=[]
    ls_kd_corner_13_time=[]
    ls_kd_corner_14_time=[]
    ls_kd_corner_15_time=[]
    ls_kd_corner_16_time=[]
    ls_kd_corner_17_time=[]
    ls_kd_corner_18_time=[]
    ls_kd_corner_19_time=[]
    ls_kd_corner_20_time = []
    for time in ls_kd_corner_time:
        ls =[]
        try:
            ls =time.replace('\'' ,'').split(',')
            ls = list(map(eval, ls))    #把列表中元素变为整形，有+号的计算
            ls.sort()               #列表从小到大排序
        except:
            ls=[]
        lenth=len(ls)
        num_goals=20
        for i in range(num_goals-lenth):
            ls.append('150')        #设定没有进球的时间为150，代表没有进球

        ls_kd_corner_1_time .append(ls[0])
        ls_kd_corner_2_time .append(ls[1])
        ls_kd_corner_3_time .append(ls[2])
        ls_kd_corner_4_time .append(ls[3])
        ls_kd_corner_5_time .append(ls[4])
        ls_kd_corner_6_time .append(ls[5])
        ls_kd_corner_7_time .append(ls[6])
        ls_kd_corner_8_time .append(ls[7])
        ls_kd_corner_9_time .append(ls[8])
        ls_kd_corner_10_time .append(ls[9])
        ls_kd_corner_11_time.append(ls[10])
        ls_kd_corner_12_time.append(ls[11])
        ls_kd_corner_13_time.append(ls[12])
        ls_kd_corner_14_time.append(ls[13])
        ls_kd_corner_15_time.append(ls[14])
        ls_kd_corner_16_time.append(ls[15])
        ls_kd_corner_17_time.append(ls[16])
        ls_kd_corner_18_time.append(ls[17])
        ls_kd_corner_19_time.append(ls[18])
        ls_kd_corner_20_time.append(ls[19])
    dic={'客_角1_时间':ls_kd_corner_1_time,
         '客_角2_时间': ls_kd_corner_2_time,
         '客_角3_时间': ls_kd_corner_3_time,
         '客_角4_时间': ls_kd_corner_4_time,
         '客_角5_时间': ls_kd_corner_5_time,
         '客_角6_时间': ls_kd_corner_6_time,
         '客_角7_时间': ls_kd_corner_7_time,
         '客_角8_时间': ls_kd_corner_8_time,
         '客_角9_时间': ls_kd_corner_9_time,
         '客_角10_时间': ls_kd_corner_10_time,
         '客_角11_时间': ls_kd_corner_11_time,
         '客_角12_时间': ls_kd_corner_12_time,
         '客_角13_时间': ls_kd_corner_13_time,
         '客_角14_时间': ls_kd_corner_14_time,
         '客_角15_时间': ls_kd_corner_15_time,
         '客_角16_时间': ls_kd_corner_16_time,
         '客_角17_时间': ls_kd_corner_17_time,
         '客_角18_时间': ls_kd_corner_18_time,
         '客_角19_时间': ls_kd_corner_19_time,
         '客_角20_时间': ls_kd_corner_20_time,
         }
    return (dic)
#01最终的进球，角球，时间，集成到一起
def fun_goal_conrner_time_all(html_soup):
    dic_times_num=_fun_get_goals_couners_num_time_1(html_soup)

    dic_zd_g=zd_goal_time(dic_times_num)
    dic_kd_g=kd_goal_time(dic_times_num)
    dic_zd_c=zd_corner_time(dic_times_num)
    dic_kd_c=kd_corner_time(dic_times_num)
    dic=dict()
    dic.update(dic_zd_g)
    dic.update(dic_kd_g)
    dic.update(dic_zd_c)
    dic.update(dic_kd_c)
    dic_times_num.pop('主_全_进球时间')
    dic_times_num.pop('客_全_进球时间')
    dic_times_num.pop('主_全_角球时间')
    dic_times_num.pop('客_全_角球时间')
    print(dic_times_num.keys())
    dic.update(dic_times_num)
    return (dic)
#检查页码中是否有下一页
def fun_get_url_next_page(html_soup):
    ##004########获取:下一页的链接##############################################################################
    next_pages = html_soup.select('#pager > ul > li > a')
    url_next_p = ''  # 设置一个默认值，找不到时不报错
    for page in next_pages:
        # /diary/20180611/p.2
        if '下一页' in page.text:
            url_next_p = page.get('href')
        else:
            url_next_p = ''
    return (url_next_p)
#把上面所有的函数结果集成到一起
def fun_main_get_id_page(html_soup):
    dic_id_name_init=fun_get_ID_name_init(html_soup)
    dic_card_pm=fun_get_Card_Pm(html_soup)
    dic_goal_cornor=fun_goal_conrner_time_all(html_soup)
    url_next_page=fun_get_url_next_page(html_soup)
    dic=dict()
    dic.update(dic_id_name_init)
    dic.update(dic_card_pm)
    dic.update(dic_goal_cornor)
    df=pd.DataFrame(dic,columns=['本场比赛ID', '联赛名称', '联赛ID', '主_名字', '主_ID', '客_名字', '客_ID',
                                 '初盘_让球', '初盘_大小', '初盘_角球', '主_黄牌', '主_红牌', '主_排名',
                                 '客_黄牌', '客_红牌', '客_排名',
                                 '主_半_比分', '客_半_比分', '主_全_比分', '客_全_比分', '主_半_角球', '客_半_角球',
                                 '主_全_角球', '客_全_角球',
                                 '主_进1_时间', '主_进2_时间', '主_进3_时间', '主_进4_时间', '主_进5_时间',
                                 '主_进6_时间', '主_进7_时间', '主_进8_时间', '主_进9_时间', '主_进10_时间',
                                 '客_进1_时间', '客_进2_时间', '客_进3_时间', '客_进4_时间', '客_进5_时间',
                                 '客_进6_时间', '客_进7_时间', '客_进8_时间', '客_进9_时间', '客_进10_时间',
                                 '主_角1_时间', '主_角2_时间', '主_角3_时间', '主_角4_时间', '主_角5_时间',
                                 '主_角6_时间', '主_角7_时间', '主_角8_时间', '主_角9_时间', '主_角10_时间',
                                 '主_角11_时间', '主_角12_时间', '主_角13_时间', '主_角14_时间', '主_角15_时间',
                                 '主_角16_时间', '主_角17_时间', '主_角18_时间', '主_角19_时间', '主_角20_时间',
                                 '客_角1_时间', '客_角2_时间', '客_角3_时间', '客_角4_时间', '客_角5_时间',
                                 '客_角6_时间', '客_角7_时间', '客_角8_时间', '客_角9_时间', '客_角10_时间',
                                 '客_角11_时间', '客_角12_时间', '客_角13_时间', '客_角14_时间', '客_角15_时间',
                                 '客_角16_时间', '客_角17_时间', '客_角18_时间', '客_角19_时间', '客_角20_时间',
                                 ])
    return (df,url_next_page)

def fun_main_get_id_page_now(html_soup):
    ##001########获取ID和名字##############################################################################
    ls_game_id = []  # 本场比赛的ID
    #当前比赛时间
    ls_game_time=[]
    # 获取名字
    ls_league_name = []
    ls_zd_name = []
    ls_kd_name = []
    # 初盘数据
    ls_init_rangqiu = []
    ls_init_daxiao = []
    # 获取相关ID，与名字

    ID_games = html_soup.select('tbody#on > tr')

    for game in ID_games:

        ls_game_id.append(game.get('id')[1:])
        texts=game.find_all('td')[0:6]
        ls_t=[]
        for t in texts:
            ls_t.append(t.text)
        #联赛名称
        ls_league_name.append(ls_t[0].strip())
        #比赛已进行时间
        if ls_t[2].strip()=='半':
            ls_game_time.append('45.5')    #特殊标记符 半为45.5
        elif "+"in ls_t[2]:
            ls_game_time.append('92')   #伤情补时
        else:
            ls_game_time.append(ls_t[2].strip()[:-1])
        #主队名称和让球
        rangqiu=re.search(r'\(.*\)',ls_t[3]).group()    #用正则表达式提取括号内的数据
        ls_zd_name.append(ls_t[3].strip())
        ls_init_rangqiu.append(rangqiu.replace('(','').replace(')',''))
        #客队名称和大小球

        daxiao=re.search(r'\(\d+.\d*\)',ls_t[5]).group()

        ls_init_daxiao.append(daxiao.replace('(','').replace(')',''))
        ls_kd_name.append(ls_t[5].strip())

    dic = {'本场比赛ID': ls_game_id,
           '联赛名称': ls_league_name,
           '当前时间':ls_game_time,
           '主_名字': ls_zd_name, '客_名字': ls_kd_name,
           '初盘_让球': ls_init_rangqiu, '初盘_大小': ls_init_daxiao,}

    df=pd.DataFrame(dic,columns=['联赛名称','本场比赛ID','当前时间','主_名字','客_名字','初盘_让球','初盘_大小'])

    return (df)

if __name__=='__main__':

    with open('temp.html', 'rb') as f1:
        html=f1.read()

    html_soup=BeautifulSoup(html,'lxml')
    fun_main_get_id_page_now(html_soup)
    # df.to_excel('result_ID.xlsx')

