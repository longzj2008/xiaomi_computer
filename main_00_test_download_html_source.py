#!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取已经结束的比赛的ID号
from selenium import webdriver
import json
import time
import pandas as pd
from bs4 import BeautifulSoup


def function_save_html(html, path=r'data\temp.html'):
    with open(path, 'wb') as f1:
        f1.write(html)
    print('保持离线html成功！')

# 调试用：读取本地html文件
def function_read_html(path=r'data\temp.html'):
    with open(path, 'rb') as f:
        html = f.read()  # 先从离线文件中读取到
    return (html)


def login_by_cookie():
    driver = webdriver.Chrome()
    # 下面的url仅仅是用于获取登陆界面
    driver.get("https://www.dszuqiu.com")
    # 方案 1：手动添加Cookie
    # driver.add_cookie({'name':'uid','value':'R-240430-fcc080a705b2daeba051ad'})

    # 方案 2：读取cookie.txt添加Cookie
    # 注意：读取cookie值，移植时注意文件路径要更改
    with open(r'data\cookie.txt', 'r', encoding='utf-8') as f:
        cont = f.read()
        cookie = json.loads(cont)
    driver.add_cookie(cookie)
    # 刷新页面
    time.sleep(1)
    driver.refresh()
    print("登陆成功")
    # 停留10s用于观察是否登陆
    time.sleep(1)
    # 关闭浏览器
    return (driver)


if __name__ == '__main__':
    # 建立一个chrome的已经登陆的浏览器，通过cookie登陆
    driver = login_by_cookie()
    # # url_main = 'https://www.dszuqiu.com'
    # # url='https://www.dszuqiu.com/race_xc/492504'  #此比赛无球权数据
    # url = 'https://www.dszuqiu.com/race_sp/492717'  #这场比赛有权数据, 数据中没有角球数据
    # url = 'https://www.dszuqiu.com/race_xc/492717'  # 这场比赛有球权数据,
    # url = 'https://www.dszuqiu.com/race_sp/492716'  #这场比赛有权数据，数据中有角球数据
    # url='https://www.dszuqiu.com/race_xc/495626'
    # url='https://www.dszuqiu.com/race_xc/495347'
    url='https://www.dszuqiu.com/race_sp/508001'
    # url='https://www.dszuqiu.com/diary/20180625'    #for fun_get_id 测试用离线数据
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    function_save_html(html)





