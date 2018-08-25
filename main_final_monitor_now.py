#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
from fun_time import time_fun

from main_01_01_download_data_now import fun_download_game_now
from main_02_00_compress_data import main_compress_data_for_now
from main_02_01_clean_data import main_clean_data
from main_02_02_make_model_data import main_make_sub_model,main_make_model_2_sp
from main_04_query import main_query_model
from main_05_manual_analyse import main_analyse,main_analyse_for_now
from main_06_wechat_send import wechat_send
from main_07_trace import main_trace_model
from main_08_yongli_check import main_download_yongli,main_check_game_in_yongli
from fun_download import DL
import itchat


import math
def init_wechat(ls_friends):
    time_mark = time_fun.time_now().strftime('%Y-%m-%d %H:%M:%S')
    itchat.send(time_mark, 'filehelper')
    itchat.send('微信登陆成功', 'filehelper')

    ls_friends = ['longzj2018']
    ls_username = []
    for name in ls_friends:
        friend = itchat.search_friends(name)
        username = friend[0].get('UserName')
        ls_username.append(username)
    return (ls_username)

def fun_download_driver_url(driver,url):
    driver.get(url)
    time.sleep(2)  # 设置延时，防止被封号
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

def check_game_45(html_soup,time_start,time_end,driver,path_download_save_folder,ls_delete_league,ls_yongli_leagues,model_name):
    # ################################################################################
    # #第一步，做参数设定
    # # #开始下载当前进行中的比赛
    folder_name = path_download_save_folder.split('\\')[1]
    file_name = folder_name + '.xlsx'
    df_result=pd.DataFrame()    #对返回值进行初始化
    ####################################################################################
    # #下载原始比赛数据
    print('下载在时间段内的原始比赛数据')
    df_state = fun_download_game_now(html_soup, time_start, time_end, driver, path_download_save_folder,
                                     ls_delete_league, ls_yongli_leagues)
    print('是否有时间段内比赛：{}'.format(df_state))
    ######################################################################
    if df_state:
        ################################################################################
        # 压缩数据
        print('#压缩数据')
        main_compress_data_for_now(path_download_save_folder)

        ################################################################################
        # 清洗数据
        print('清洗数据')
        df_now_clean=main_clean_data(path_download_save_folder)

        ################################################################################
        # 生产基础模型2
        print('生成模型2_sp')
        if 'model_2_sp' in model_name:
            df_state = main_make_model_2_sp(folder_name)
        elif 'model_2' in model_name:
            df_state = main_make_model_2(folder_name)
        else:
            print('生成基础模型时，出错')

        ################################################################################
        # 基于模型1，生产模型1_1
        if df_state:  # 为真时，存在比赛，为假时，不存在比赛
            # print('基于模型2，生产模型2_1_3')
            # df_state=main_make_sub_model('now','model_2','model_2_1_3','半球和',0.5,3.5)
            # ################################################################################
            # #进行查询
            # if df_state:    #为真时，存在比赛，为假时，不存在比赛
            print('进行查询')
            model_name = 'model_2_sp'
            lenth = 408 - 6 #模型2的长度
            path_result = 'ds_data_test\\' + model_name + '\\' + 'test_result' + '\\' + file_name
            ############################################
            try:
                df_query_last = pd.read_excel(path_result)  # 读取上次now的数据
            except:
                print('没有上次结果')
                df_query_last=pd.DataFrame()

            df_query = main_query_model(file_name, model_name, lenth)

            try:
                # flag_same = (df_query_last['激发量'] == df_query['激发量']).all()  # 代表这次判断是否和上次一样
                flag_same = (df_query_last['激发量'] == df_query['激发量']).all()  # 代表这次判断是否和上次一样
            except:
                flag_same = False
            print('now数据与上次是否相同：{}'.format(flag_same))
            ###############################################
            if not flag_same:  # 如果和上次不一样，代表有新的比赛出现
                ################################################################################
                ls_last = list(df_query_last['本场比赛ID']) #上一次的
                ls_now_tmp = list(df_query['本场比赛ID'])   #这一次的
                ls_now_check = []       #这一次不在上一次的部分
                for xx_tmp in ls_now_tmp:
                    if not xx_tmp in ls_last:   #还上次保存的不一样的id
                        ls_now_check.append(xx_tmp)
                ################################################################################
                # 进行分析
                print('进行筛选分析')
                df_result=main_analyse_for_now(model_name)
                print('分析结果如下')
                print(ls_now_check)
                print(df_result)
                print('@@' * 20)
                ###############################################################################

                try:    #进行筛选，只发送上次，没有发送的部分
                    for id_del in ls_now_check:
                        df_result = df_result[df_result['本场比赛ID'] != id_del]
                except:
                    print('在筛选微信发送结果时，出错')
                    df_result=pd.DataFrame()
                    pass
                ###############################################################################
                # ls_columns_send=['联赛名称','主队名称','客队名称','预测结果','激发量','真实结果']
                if not df_result.empty:
                    #######################################################################
                    #进行微信发送
                    print('开始微信发送')
                    wechat_send('下面是半场判断结果', lifesign_wechat, ls_username)
                    for name in df_result['主队名称']:
                        if not name=='':
                            time.sleep(1)
                            info = df_result[df_result['主队名称'] == name].to_json(orient='index', force_ascii=False)
                            wechat_send(info, lifesign_wechat, ls_username)

                    print('#' * 20)
                    print('微信发送成功')
                    print('#' * 20)
                else:
                    print('可判断的结果为空')

            else:
                print('本次now数据与上次一样，微信不再发送')
        else:
            print('没有符合标准的比赛，等待进入下一次检测')
    else:
        print('没有在时间段内的比赛')

    return (df_result)
    pass

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

    ##￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
    #参数设置区
    # ################################################################################
    # 这里控制了下载比赛的时间段
    time_start = 50  # 45.5为特殊的标记符，代表“半”
    time_end = 80
    #删除没有盘口的联赛,在下载now函数中增加
    ls_delete_league=[]
    #增加一些需要跟踪的比赛id
    # ################################################################################
    #登陆微信
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    ##########################################
    #初始化微信，生成username
    ls_friends=['longzj2018']
    ls_username=init_wechat(ls_friends)
    lifesign_wechat = 0
    ##################################################################################
    # 建立一个chrome的已经登陆的浏览器，通过cookie登陆
    driver = login_by_cookie()
    url_now='https://live.dszuqiu.com/'
    #记录有开机之后所有的有2球的ID，形成一个列表
    df_you2_all=pd.DataFrame()

    count=0
    time_wait = 60  # 运行一次等待的最小时间
    ls_yongli_leagues=[]
    df_results=pd.DataFrame()
    while True:
        #############################################################################################
        #每个1，更新now列表
        html_soup = DL.fun_download_driver_url(driver, url_now)
        #############################################################################################
        #每个2，对微信生命信号检查
        if count%2==0: #5*time_wait #
            print('每隔2，发送微信生命信号')
            try:
                #####################################################################################
                # wechat 的生命信号
                lifesign_wechat += 1
                time_mark = time_fun.time_now().strftime('%Y-%m-%d %H:%M:%S')
                itchat.send(time_mark, 'filehelper')
                itchat.send(str(lifesign_wechat), 'filehelper')
                #####################################################################################
            except:
                itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
                ls_username=init_wechat(ls_friends)
        #############################################################################################
        #每个10，对永利盘口进行检查
        if count%30==0: #每30分钟对永利含有的比赛进行检查
            print('每隔10,检查永利所有有盘口比赛')
            ls_yongli_leagues=main_download_yongli(driver)
            print('永利有盘口的比赛有{}'.format(ls_yongli_leagues))
            pass

        #############################################################################################
        #每个3，对半场数据进行检查
        if count%3==0:#每隔3分钟检查一次,对半场数据进行大2 判断
            print('每隔3，对半场数据进行判断')
            path_download_save_folder = 'football_data\\now\\'
            model_name='model_2_sp'
            df_result_single=check_game_45(html_soup, time_start, time_end, driver, path_download_save_folder, ls_delete_league,
                          ls_yongli_leagues,model_name)
            df_results=df_results.append(df_result_single)
            #######################################################################
            # 对结果进行连续保存
            path_trace = 'data\\' + model_name + '_trace.xlsx'
            print('需要跟踪的比赛，保存路径为{}'.format(path_trace))
            df_results.to_excel(path_trace)

        if count%1==0:   #每个60s检查一次
            ###########################################################################################
            ##进行一次跟踪
            print('检查是否有追踪的比赛,跨球小于等于预测值')
            model_name='model_2_sp'
            path_trace='data\\'+model_name+'_trace.xlsx'
            trace_game_45(path_trace,html_soup,driver)
            # except:
            #     print('trace 出错')

        #########################################################################################
        count=count+1
        print('一轮运行结束')
        time.sleep(time_wait)
        print('#'*30)












