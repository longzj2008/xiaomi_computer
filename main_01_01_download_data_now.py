#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
#获取比赛ID
from fun_get_id import main_get_id
from fun_time import time_fun
from fun_get_sp_xc import main_get_sp_xc
from fun_get_sp_xc import main_get_xc_table
from main_08_yongli_check import main_check_game_in_yongli
from fun_download import DL

def fun_del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

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

def fun_download_driver_url(driver,url):
    driver.get(url)
    time.sleep(3)  # 设置延时，防止被封号
    html = driver.page_source.encode('utf-8')
    html_soup = BeautifulSoup(html, 'lxml')
    return (html_soup)

#######################################################
#删除没有盘口的比赛
def __fun_02_del_str(df,s='友谊'):
    # df=df.astype('str')
    df1=df[df['联赛名称'].str.contains(s)]
    ls_id=list(df1['本场比赛ID'])
    for id in ls_id:
        df=df[df['本场比赛ID']!=id]
    return (df)

#跟踪下载当前符合要求的比赛
def fun_download_game_now(html_soup, time_start, time_end, driver, path_download_save,ls_delete_league,ls_yongli_leagues):

    ###########################################################################################################
    #先清空文件夹
    # fun_del_file('ds_data_now')

    ############################################################################################################
    # 调用函数，获取ID等信息
    ############################################################################################################
    df_id_orginal = main_get_id.fun_main_get_id_page_now(html_soup)  # 注意这个函数返回两个参数
    df_id_orginal['当前时间']=df_id_orginal['当前时间'].astype('float')
    #############################################################################################################
    #删除联赛中，手动指定的，没有盘口的联赛
    for league_name in ls_delete_league:
        if not league_name=='':
            df_id_orginal=__fun_02_del_str(df_id_orginal,league_name)
    #############################################################################################################
    # 删除永利中没有的比赛
    pass
    for league_name in df_id_orginal['联赛名称']:
        flag=main_check_game_in_yongli(league_name,ls_yongli_leagues)
        if flag=='yes':
            print('联赛名称：{} 在永利中有盘口'.format(league_name))
            pass
        else:
            df_id_orginal=__fun_02_del_str(df_id_orginal,league_name)
    #############################################################################################################
    #从数据中帅选出有买入时间点的比赛，并存表
    df_30=df_id_orginal[((df_id_orginal['当前时间']>=time_start) & (df_id_orginal['当前时间']<=time_end))]
    #############################################################################################################
    #重置行索引
    df_30.reset_index(drop=True,inplace=True) # column 改为从0开始
    ###################################################
    path_save_prefix=path_download_save
    url_main='https://www.dszuqiu.com'
    ####################################################
    file_name = 'model0' + str(time_start)
    path_ds_data = path_save_prefix + 'ds_data\\'
    fun_del_file(path_ds_data)  # 清空一下ds_data文件夹
    path_ds_data_filename = path_save_prefix + 'ds_data\\' + file_name + '.csv'
    
    if not df_30.empty:

        df_30.to_csv(path_ds_data_filename,encoding='utf-8')
        # 计数
        num_id = len(df_30['本场比赛ID'])
        n = 1  # 从1开始
        df_xc_all=pd.DataFrame()
        for id in df_30['本场比赛ID']:
            print(id)
            print('本页id总数:{}，当前id序号:{}'.format( num_id, n))
            n += 1
            sr_xc_id=DL.download_sp41_xc_table_base_id(id,driver,path_save_prefix,file_name)
            df_xc_all = df_xc_all.append(sr_xc_id, ignore_index=True)  # df append()之后，必需重新赋值给df，不然df还使用原来的
        #############################################################################################################
        df_end = df_30.join(df_xc_all)
        #############################################################################################################
        # 重置行索引
        df_end.reset_index(drop=True,inplace=True)
        #############################################################################################################
        path = path_ds_data_filename
        df_end.to_csv(path)
        #返回所有下载的ID的当前时间，共压缩后，查询sp大小值
    return (not df_30.empty)

def fun_download_game_trace(html_soup, driver, path_save_folder,df_check):
    ###########################################################################################################
    # 先清空文件夹
    # fun_del_file('ds_data_now')
    ############################################################################################################
    # 调用函数，获取ID等信息
    ############################################################################################################
    df_id_orginal = main_get_id.fun_main_get_id_page_now(html_soup)
    print('#05')
    print(df_id_orginal)
    df_id_orginal['当前时间'] = df_id_orginal['当前时间'].astype('float')
    df_id_orginal['本场比赛ID'] = df_id_orginal['本场比赛ID'].astype('int')
    #############################################################################################################
    # 从数据中帅选出有买入时间点的比赛，并存表
    df_30 = df_id_orginal[((df_id_orginal['当前时间'] >= 30) & (df_id_orginal['当前时间'] <= 85))]
    df_30.to_excel('now_games.xlsx')
    #############################################################################################################
    #与df_check进行比较，看是否存在,
    ls_id_check=list(df_check['本场比赛ID'])
    print(ls_id_check)
    df_30=df_30[df_30['本场比赛ID'].isin(ls_id_check)]
    #############################################################################################################
    # 重置行索引
    df_30.reset_index(drop=True,inplace=True)  # column 改为从0开始
    df_30.to_excel('222.xlsx')
    ############################################################################################################
    path_save_prefix = path_save_folder
    url_main = 'https://www.dszuqiu.com'
    ############################################################################################################
    file_name = 'model0' + 'tr'     #用于标识用途
    path_ds_data = path_save_folder + 'ds_data\\'
    ############################################################################################################
    fun_del_file(path_ds_data)  # 清空一下ds_data文件夹
    path_ds_data_filename = path_save_folder + 'ds_data\\' + file_name + '.csv'
    ###########################################################################################################
    if not df_30.empty:
        #df_30.to_csv(path_ds_data_filename, encoding='utf-8')
        # 计数
        num_id = len(df_30['本场比赛ID'])
        n = 1  # 从1开始
        df_xc_all = pd.DataFrame()
        ls_delete_abnormal=[]
        for id in df_30['本场比赛ID']:
            print(id)
            print('本页id总数:{}，当前id序号:{}'.format(num_id, n))
            n += 1
            sr_xc_id = DL.download_sp41_xc_table_base_id(id, driver, path_save_prefix, file_name)
            df_xc_all = df_xc_all.append(sr_xc_id, ignore_index=True)  # df append()之后，必需重新赋值给df，不然df还使用原来的
        ###############################################################################################################
        #合并ID 数据 和xc的图文数据
        df_id_init_xc = df_30.join(df_xc_all)
        ###############################################################################################################
        #删除提取sp41 和 xc_tabel数据有问题的ID
        ls_delete_abnormal=list(set(ls_delete_abnormal))
        print('需要删除的比赛ID有：{}'.format(ls_delete_abnormal))
        if len(ls_delete_abnormal) > 0:
            for id_del in ls_delete_abnormal:
                df_id_init_xc = df_id_init_xc[df_id_init_xc['本场比赛ID'] != id_del]
        ###############################################################################################################
        #重置一下索引
        df_id_init_xc.reset_index(drop=True,inplace=True)
        ###############################################################################################################
        #存储
        path = path_ds_data_filename
        df_id_init_xc.to_csv(path)
        # 返回所有下载的ID的当前时间，共压缩后，查询sp大小值
    else:
        print('没有需要跟踪的比赛数据')
        df_id_init_xc=pd.DataFrame()
    return (df_id_init_xc)

def fun_download_game_trace_all(html_soup, driver, path_save_folder):
    ###########################################################################################################
    # 先清空文件夹
    # fun_del_file('ds_data_now')
    ############################################################################################################
    # 调用函数，获取ID等信息
    ############################################################################################################
    df_id_orginal = main_get_id.fun_main_get_id_page_now(html_soup)  # 注意这个函数返回两个参数
    df_id_orginal['当前时间'] = df_id_orginal['当前时间'].astype('float')
    df_id_orginal['本场比赛ID'] = df_id_orginal['本场比赛ID'].astype('int')
    #############################################################################################################
    # 从数据中帅选出有买入时间点的比赛，并存表
    df_30 = df_id_orginal[((df_id_orginal['当前时间'] >= 10) & (df_id_orginal['当前时间'] <= 80))]
    #############################################################################################################
    # 重置行索引
    df_30.reset_index(drop=True,inplace=True)  # column 改为从0开始
    ############################################################################################################
    url_main = 'https://www.dszuqiu.com'
    ############################################################################################################
    file_name = 'model0' + 'tr'
    path_ds_data = path_save_folder + 'ds_data\\'
    ############################################################################################################
    fun_del_file(path_ds_data)  # 清空一下ds_data文件夹
    path_ds_data_filename = path_save_folder + 'ds_data\\' + file_name + '.csv'
    ###########################################################################################################
    if not df_30.empty:
        #df_30.to_csv(path_ds_data_filename, encoding='utf-8')
        # 计数
        num_id = len(df_30['本场比赛ID'])
        n = 1  # 从1开始
        df_xc_all = pd.DataFrame()
        ls_delete_abnormal=[]
        for id in df_30['本场比赛ID']:
            print(id)
            print('本页id总数:{}，当前id序号:{}'.format(num_id, n))
            n += 1
            url_id = url_main + r'/race_xc/' + str(id)
            print(url_id)
            html_soup = fun_download_driver_url(driver, url_id)
            ############################################################################################################
            # 提取ID现场 中的 图文信息及半场，全场数据信息
            ############################################################################################################
            sr_xc_id, error = main_get_sp_xc.fun_main_get_data_xc(html_soup)
            df_xc_all = df_xc_all.append(sr_xc_id, ignore_index=True)  # df append()之后，必需重新赋值给df，不然df还使用原来的
            # df_xc_all.to_excel(str(n)+'_'+'501481.xlsx')
            ############################################################################################################
            # 下载ID中的xc_table 表格信息
            ############################################################################################################
            try:
                df_xc_table = main_get_xc_table.fun_main_adjust_gongfang_table(html_soup)
            except:
                df_xc_table = pd.DataFrame()
                ls_delete_abnormal.append(id)
            path = path_save_folder + 'ds_data_xc_table\\' + file_name + '_' + str(id) + '.csv'
            df_xc_table.to_csv(path, encoding='utf-8')
            ############################################################################################################
            # 下载 sp41 数据
            ############################################################################################################
            url_id = url_main + r'/race_sp/' + str(id)
            print(url_id)
            html_soup = fun_download_driver_url(driver, url_id)
            try:
                df_sp41 = main_get_sp_xc.fun_main_get_data_sp(html_soup)
            except:
                df_sp41=pd.DataFrame()
                ls_delete_abnormal.append(id)
            path = path_save_folder + 'ds_data_sp41\\' + file_name + '_' + str(id) + '.csv'
            df_sp41.to_csv(path)
        ###############################################################################################################
        #合并ID 数据 和xc的图文数据
        df_id_init_xc = df_30.join(df_xc_all)
        ###############################################################################################################
        #删除提取sp41 和 xc_tabel数据有问题的ID
        ls_delete_abnormal=list(set(ls_delete_abnormal))
        print('需要删除的比赛ID有：{}'.format(ls_delete_abnormal))
        if len(ls_delete_abnormal) > 0:
            for id_del in ls_delete_abnormal:
                df_id_init_xc = df_id_init_xc[df_id_init_xc['本场比赛ID'] != id_del]
        ###############################################################################################################
        #重置一下索引
        df_id_init_xc.reset_index(drop=True,inplace=True)
        ###############################################################################################################
        #存储
        path = path_ds_data_filename
        df_id_init_xc.to_csv(path)
        # 返回所有下载的ID的当前时间，共压缩后，查询sp大小值
    else:
        print('没有需要跟踪的比赛数据')
        df_id_init_xc=pd.DataFrame()
    return (df_id_init_xc)

if __name__=='__main__':
    #建立一个chrome的已经登陆的浏览器，通过cookie登陆

    driver=login_by_cookie()
    url_now='https://live.dszuqiu.com/'

    html_soup=fun_download_driver_url(driver,url_now)
    #
    #
    # with open('data\\temp.html','r',encoding='utf-8') as f:
    #     html=f.read()
    # html_soup = BeautifulSoup(html, 'lxml')
    # # #开始下载当前进行中的比赛
    # path_download_save='football_data\\now\\'
    # time_start=20
    # time_end=30
    # fun_download_game_now(html_soup,time_start,time_end,driver,path_download_save)
    path_download_save = 'football_data\\now\\'
    fun_download_game_now(html_soup,40,60,driver,path_download_save)