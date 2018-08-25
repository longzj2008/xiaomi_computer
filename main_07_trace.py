#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
from fun_time import time_fun
from fun_make_table import make_sp_xc_table

from main_01_01_download_data_now import fun_download_game_trace,fun_download_game_trace_all
from main_02_00_compress_data import  main_compress_data_for_now
def fun_download_driver_url(driver,url):
    driver.get(url)
    time.sleep(1)  # 设置延时，防止被封号
    html = driver.page_source.encode('utf-8')
    html_soup = BeautifulSoup(html, 'lxml')
    return (html_soup)

def login_by_cookie():

    driver = webdriver.Chrome()
    #下面的url仅仅是用于获取登陆界面
    driver.get("https://www.dszuqiu.com")
    # 方案 1：手动添加Cookie
    # driver.add_cookie({'name':'uid','value':'R-240430-fcc080a705b2daeba051ad'})

    #方案 2：读取cookie.txt添加Cookie
    # 注意：读取cookie值，移植时注意文件路径要更改
    with open(r'data\cookie.txt', 'r', encoding='utf-8') as f:
        cont = f.read()
        cookie = json.loads(cont)
    driver.add_cookie(cookie)
    # 刷新页面
    time.sleep(1)
    driver.refresh()
    print("登陆成功")
    #停留10s用于观察是否登陆
    time.sleep(1)
    #关闭浏览器
    return (driver)

def fun_find_time_sp(df_input,path_read_folder):
    df_input.reset_index(drop=False, inplace=True)  # df_input 已经在上一步的download中重置过了
    df_input['当前时间']=df_input['当前时间'].astype('int')
    df_end_tmp=pd.DataFrame()
    for id in df_input['本场比赛ID']:  # 每一个id获取生成一个序列
        df_id_single = df_input[df_input['本场比赛ID'] == id]
        ls_time = list(df_id_single['当前时间'])

        ################################################################################################################
        # 从 ds_data_sp41 中提取每一个id的sp数据
        ###############################################################################################################
        path = path_read_folder + 'ds_data_sp41\\' + 'model0tr'+ '_' + str(id) + '.csv'

        # 读取文件,生成df_sp
        try:
            df_sp,abnormal_id=make_sp_xc_table.make_sp_table(path)

            ###########################################################################################################
            #提取当前比赛时间点的数据
            df_sp_time = df_sp[df_sp['比赛时间'].isin(ls_time)]
            # print(df_sp_time)
            df_end_tmp=df_end_tmp.append(df_sp_time)
        except:
            print('trace sp data 时，出错')
    #重置索引，便于后面进行合并
    df_end_tmp.reset_index(drop=False,inplace=True)
    df_output=df_end_tmp.copy()

    return (df_output)

def fun_xc_add_parameter(df_xc_table):

    pass

def fun_find_time_xc(df_input,path_read_folder):

    df_input.reset_index(drop=False, inplace=True)  # df_input 已经在上一步的download中重置过了
    df_input['当前时间'] = df_input['当前时间'].astype('int')
    df_end_tmp = pd.DataFrame()
    for id in df_input['本场比赛ID']:  # 每一个id获取生成一个序列
        df_id_single = df_input[df_input['本场比赛ID'] == id]
        ls_time = list(df_id_single['当前时间'])
        print(ls_time)
        ################################################################################################################
        # 从 ds_data_xctable中提取每一个id的sp数据
        ###############################################################################################################
        path = path_read_folder + 'ds_data_xc_table\\' + 'model0tr' + '_' + str(id) + '.csv'
        print(path)
        try:
            df_xc_table,abnormal_id=make_sp_xc_table.make_xc_table(path)
            ###########################################################################################################
            df_xc_table_time = df_xc_table[df_xc_table['时间'].isin(ls_time)]
            # print(df_xc_table_time)
            df_end_tmp=df_end_tmp.append(df_xc_table_time)
        except:
            print('trace xc_table数据时，出错')

    df_end_tmp.reset_index(drop=False, inplace=True)
    df_output=df_end_tmp.copy()

    return (df_output)

def fun_adjust(df):

    # ls_all = ['本场比赛ID', '联赛名称_x', '主队名称', '客名_跨值', '预测结果_x', '得分',
    #          'level_0', 'index_x', '联赛名称_y', '当前时间', '主_名字', '客_名字', '初盘_让球',
    #          '初盘_大小', '主_全_危险进攻', '主_全_射偏', '主_全_射正', '主_全_球权', '主_全_进攻',
    #          '主_半_危险进攻', '主_半_射偏', '主_半_射正', '主_半_球权', '主_半_进攻', '场地情况',
    #          '天气情况', '客_全_危险进攻', '客_全_射偏', '客_全_射正', '客_全_球权', '客_全_进攻',
    #          '客_半_危险进攻', '客_半_射偏', '客_半_射正', '客_半_球权', '客_半_进攻', '红牌数量和',
    #          '红牌时间', '角球数量和', '角球时间', '进球数量和', '进球时间', '黄牌数量和', '黄牌时间',
    #          'index_y', '主_大小_球数', '客_大小_球数', '主_大小_水', '大小球', '客_大小_水', '主_让分_水',
    #          '让分球', '客_让分_水', '主_角球_球数', '客_角球_球数', '主_角球_水', '角球球', '客_角球_水',
    #          '主_胜平负_水', '胜平负球', '客_胜平负_水', '比赛时间', 'index', '时间', '主_角球_数量',
    #          '客_角球_数量', '主_射正_数量', '客_射正_数量', '主_进球_数量', '客_进球_数量', '主_射偏_数量',
    #          '客_射偏_数量', '主_危险进攻_数量', '客_危险进攻_数量', '主_进攻_数量', '客_进攻_数量']

    df['真实球和']=df['主_大小_球数']+df['客_大小_球数']
    df['盘口球和']=df['大小球']
    df['球和跨值']=df['盘口球和']-df['真实球和']
    df['买大水']=df['主_大小_水']

    #####################################################################
    df['初盘_大小']=df['初盘_大小'].astype('float')
    #####################################################################
    df['主_危进比客_危进']=df['主_危险进攻_数量']/df['客_危险进攻_数量']
    df['主_危进比时间']=df['主_危险进攻_数量']/df['当前时间']
    df['客_危进比时间'] = df['客_危险进攻_数量'] / df['当前时间']
    ################################################################
    df['主角球比时间']=df['主_角球_球数']/df['当前时间']
    df['客角球比时间'] = df['客_角球_球数'] / df['当前时间']
    ################################################################
    df['主_射门和']=df['主_射正_数量']+df['主_射偏_数量']
    df['客_射门和'] = df['客_射正_数量'] + df['客_射偏_数量']
    df['主_射门和比时间'] = df['主_射门和'] / df['当前时间']
    df['客_射门和比时间'] = df['客_射门和'] / df['当前时间']
    #################################################################
    df['主_射正比射偏']=df['主_射正_数量']/df['主_射偏_数量']
    df['客_射正比射偏'] = df['客_射正_数量'] / df['客_射偏_数量']


    #################################################################
    #排除的比赛如下：
    #00  排除初盘小于2.5的比赛

    df=df[df['初盘_大小']>=2]
    #01  危险进攻过多，小于1，代表时间大，危险进攻少
    df=df[df['主_危进比时间']<1]
    df = df[df['客_危进比时间'] < 1]
    #02  角球过多的比赛 频率：每5分钟可以有一个角球,两个球队都很多
    # df=df[((df['主角球比时间']*5)<1)&((df['客角球比时间']*5) < 1)]      #双方都有很多角球，都大于半场大于7个
    # df=df[(df['主角球比时间']*4.5)<=1]         #或者一方多余10个
    # df = df[(df['客角球比时间'] * 4.5) <=1]  #或者一方多余10个
    # #03  不能一直没有射门,任一球队 频率：每10分钟一个有射正或射偏
    # df = df[((df['主_射门和比时间']*10) > 1)|((df['客_射门和比时间']*10) > 1)]
    #04  射正比射偏小于 1/2的，双方进攻阻力都太大
    # df=df[(df['主_射正比射偏']>=0.3)|(df['客_射正比射偏']>=0.3)]
    #05  排除把大巴的
    df=df[(df['主_危进比客_危进']<1.5) | (df['主_危进比客_危进']>0.66)]
    #04  球和跨值 跨值1.75 时间小于50， 跨值0.75，时间小于70
    # df=df[((df['球和跨值']<=1.75)&(df['当前时间']<=48))|((df['球和跨值'] <= 0.75) & (df['当前时间'] <= 70))]

    ls_end=['当前时间','联赛名称_x', '主队名称', '预测结果_x', '得分', '球和跨值', '买大水',
          '让分球']
    df=df.reindex(columns=ls_end)
    return (df)

def main_trace_model(html_soup,driver,path_read):
    ########################################################
    df_check=pd.read_excel(path_read)  #读取后
    if not df_check.empty:
        ######################################################
        #sort 根据激发量
        df_check = df_check.sort_values(by='得分')
        #去重 根据id 不需要重新赋值
        df_check.drop_duplicates(subset=['本场比赛ID'], keep='last', inplace=True)
        #重置索引
        df_check=df_check.reset_index(drop=True)

        ########################################################

        path_trace_download_folder='football_data\\trace\\'
        df_id_init_xc=fun_download_game_trace(html_soup,driver,path_trace_download_folder,df_check)

        ########################################################
        if not df_id_init_xc.empty:
            df_sp41=fun_find_time_sp(df_id_init_xc,path_trace_download_folder)

            df_xc_table=fun_find_time_xc(df_id_init_xc,path_trace_download_folder)
            df_tmp=pd.merge(df_id_init_xc, df_sp41, left_index=True, right_index=True, how='outer')
            df_t=pd.merge(df_tmp, df_xc_table, left_index=True, right_index=True, how='outer')
            print('#05')
            print(list(df_t.columns))
            df=pd.merge(df_check,df_t,left_on='本场比赛ID',right_on='本场比赛ID',how='inner')
            print('#06')
            print(list(df.columns))
            df.to_excel('trace_before_adjust.xlsx')
            df=fun_adjust(df)
            df.to_excel('trace_after_adjust.xlsx')
            print('#07')
            print(list(df.columns))

        else:
            df = pd.DataFrame()
    else:
        df=pd.DataFrame()

    return (df)

# def main_trace_all(html_soup,driver):
#
#
#     path_trace_download_folder='football_data\\trace\\'
#     df_id_init_xc=fun_download_game_trace_all(html_soup,driver,path_trace_download_folder)
#     if not df_id_init_xc.empty:
#         df_sp41=fun_find_time_sp(df_id_init_xc,path_trace_download_folder)
#         df_xc_table=fun_find_time_xc(df_id_init_xc,path_trace_download_folder)
#         df_tmp=pd.merge(df_id_init_xc, df_sp41, left_index=True, right_index=True, how='outer')
#         df=pd.merge(df_tmp, df_xc_table, left_index=True, right_index=True, how='outer')
#         # df.to_excel('111.xlsx')
#         df=fun_adjust_decide(df)
#         df.to_excel('data\\trace.xlsx')
#         ls_end = ['联赛名称', '当前时间', '主_名字', '客_名字', '初盘_大小', '球和跨值', '买大水']
#         df = df.reindex(columns=ls_end)
#     else:
#         df = pd.DataFrame()
#     return (df)

def trace_game_45(path_trace,html_soup,driver):

    df_trace = main_trace_model(html_soup, driver,path_trace)
    print('追踪的比赛有{}'.format(df_trace))
    if not df_trace.empty:
    ##############################################
        path_trace_equal = 'data\\trace_equal.xlsx'
        try:
            df_trace_equal_last = pd.read_excel(path_trace)
        except:
            df_trace_equal_last=pd.DataFrame()

    #################################################
        df_trace_equal = df_trace[df_trace['预测结果_x'] == df_trace['球和跨值']]
        df_trace_equal.to_excel(path_trace_equal)
        ##############################
        flag_trace=False
        try:
            flag_trace = (df_trace_equal_last['球和跨值'] == df_trace_equal['球和跨值']).all()  # 代表这次判断是否和上次一样
        except:
            flag_trace = False
        ##############################################################################
        # 在追踪的，有机会的比赛
        if (not df_trace_equal.empty) and (not flag_trace):
            print('下面为追踪的比赛情况：')
            print(df_trace_equal)
            wechat_send('下面是追踪结果', lifesign_wechat, ls_username)
            for name in df_trace_equal['主队名称']:
                info_trace = df_trace_equal[df_trace_equal['主队名称'] == name].to_json(orient='index', force_ascii=False)
                wechat_send(info_trace, lifesign_wechat, ls_username)
            print('#' * 20)
            print('微信发送成功')
            print('#' * 20)

        else:
            print('追踪的比赛,不满足发送条件：1、预测=跨值；2、与上次一样')
    else:
        print('当前没有可追踪的比赛')
    pass

if __name__=='__main__':
    pass
    #建立一个chrome的已经登陆的浏览器，通过cookie登陆
    driver = login_by_cookie()
    url_now = 'https://live.dszuqiu.com/'
    while 1:
        time.sleep(10)
        html_soup = fun_download_driver_url(driver, url_now)

        print('检查是否有追踪的比赛,跨球小于等于预测值')
        model_name = 'model_2_sp'
        path_trace = 'data\\' + model_name + '_trace.xlsx'
        trace_game_45(path_trace, html_soup, driver)



