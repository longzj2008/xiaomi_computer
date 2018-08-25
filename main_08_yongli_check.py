#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import time


def function_save_html(html,path=r'data\temp.html'):

    with open(path,'wb') as f1:
        f1.write(html)
    print('保持离线html成功！')

#调试用：读取本地html文件
def function_read_html(path=r'data\temp.html'):
    with open(path, 'rb') as f:
        html = f.read()  # 先从离线文件中读取到
    return (html)

def fun_download_driver_url(driver,url):
    driver.get(url)
    time.sleep(2)  # 设置延时，防止被封号
    html = driver.page_source.encode('utf-8')
    function_save_html(html)
    html_soup = BeautifulSoup(html, 'lxml')
    return (html_soup)

def main_download_yongli(driver):
    ##############################################
    url = 'https://3050.mk/hg_sports/index/ft/gq'
    html_soup=fun_download_driver_url(driver, url)

    leagues = html_soup.select('#data > tbody > tr > td.b_title')
    ls_leagues = []
    for league in leagues:
        ls_leagues.append(league.text)
        print(league.text)
    return (ls_leagues)

def main_check_game_in_yongli(league_name,ls_leagues):

    flag_youwu = 'no'
    for name in ls_leagues:
        ls_true = []
        for zi in league_name:
            if zi in name:
                ls_true.append(True)
            else:
                ls_true.append(False)

        if all(ls_true):
            flag_youwu = 'yes'
            break
        else:
            flag_youwu = 'no'

    return (flag_youwu)


if __name__=='__main__':
    driver = webdriver.Chrome()
    ls_leagues=main_download_yongli(driver)
    print(ls_leagues)
    league_name = '委内杯'
    #里约杯
    ls_league_name=['委内杯','里约杯']
    for league_name in ls_league_name:
        flag=main_check_game_in_yongli(league_name,ls_leagues)
        print(flag)