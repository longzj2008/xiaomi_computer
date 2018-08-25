#!/usr/bin/env python
# -*- coding:utf-8 -*-
#获取已经结束的比赛的ID号
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random
from fun_download import DL

def fun_download_driver_url(driver,url):
    driver.get(url)
    t=random.randint(20,30)
    time.sleep(t/10)  # 设置延时，防止被封号
    html = driver.page_source.encode('utf-8')
    html_soup = BeautifulSoup(html, 'lxml')
    return (html_soup)

def function_save_html(html,path=r'data\temp.html'):

    with open(path,'wb') as f1:
        f1.write(html)
    print('保持离线html成功！')

def function_Event_log_record(error):
    if error == 1:
        with open('data\ErrorLog.txt', 'a') as f:
            f.write(url_id)

#调试用：读取本地html文件
def function_read_html(path=r'data\temp.html'):
    with open(path, 'rb') as f:
        html = f.read()  # 先从离线文件中读取到
    return (html)

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

#获取比赛ID
from fun_get_id import main_get_id
from fun_time import time_fun
from fun_download import DL
from fun_get_sp_xc import main_get_sp_xc
from fun_get_sp_xc import main_get_xc_table

if __name__=='__main__':
    #建立一个chrome的已经登陆的浏览器，通过cookie登陆
    date_till=input('请输入截至日期：')
    num = input('请输入向前查询的天数：')
###################################################################
    #控制存放的路径
    path_save_prefix='football_data\\test\\'
    #记录程序开始运行的时间
    time_start=time_fun.time_now()
    #启动chorme浏览器，并通过cookie登陆
    driver=login_by_cookie()
    url_main='https://www.dszuqiu.com'
    ls_url_date=time_fun.url_date_list(date_till,num)
    print(ls_url_date)
    num_date=len(ls_url_date)
    for date in ls_url_date:
        n=0
        while 1:
            df_xc_all=pd.DataFrame()
            url_date = url_main + date
            #date_path是一个纯日期，date 包含/diary/日期
            date_path=date.replace('/', '').replace('.', '')[5:]
            print(url_date)
            driver.get(url_date)
            time.sleep(2)   #设置延时，防止被封号
            #把浏览器读取到的数据转换成网页格式，然后用beautifulsoup 解析
            html = driver.page_source.encode('utf-8')
            html_soup = BeautifulSoup(html, 'lxml')
            ############################################################################################################
            #调用函数，获取ID等信息
            ############################################################################################################
            df_id,url_next_p=main_get_id.fun_main_get_id_page(html_soup)    #注意这个函数返回两个参数
            #计数
            num_id=len(df_id['本场比赛ID'])
            n=1 #从1开始
            for id in df_id['本场比赛ID']:
                print(id)
                print('日期个数为:{},当前为:{},本页id总数:{}，当前id序号:{}'.format(num_date,date_path,num_id,n))
                n+=1
                ################################################################################
                #下载xc表格数据，下载sp41表格数据，返回xc图文数据
                sr_xc_id=DL.download_sp41_xc_table_base_id(id,driver,path_save_prefix,date_path)
                df_xc_all = df_xc_all.append(sr_xc_id, ignore_index=True)  # df append()之后，必需重新赋值给df，不然df还使用原来的
            # df_xc_all.to_excel('dfxcall.xlsx')    #检查天气是信息是否显示
            path =path_save_prefix+ 'ds_data/' + date_path + '.csv'
            df_end=df_id.join(df_xc_all)
            df_end.to_csv(path)

        #以下为循环的控制逻辑
            if url_next_p=='':
                break
            else:
                date=url_next_p

    #计算程序运行时间
    time_end=time_fun.time_now()
    yongshi=time_end-time_start
    print('程序执行用时：{}'.format(yongshi))


