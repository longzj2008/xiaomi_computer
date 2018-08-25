#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName : getLoginCookie.py
# Author   : Adil
# DateTime : 2018/3/20 21:43
# SoftWare : PyCharm
import time,os
import json

from selenium import webdriver

def get_login_cookie(url='https://www.dszuqiu.com/race_sp/492501'):
    # url = 'https://www.dszuqiu.com/race_sp/492501'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    driver.find_element_by_id("zhanghu").clear()
    driver.find_element_by_id("zhanghu").send_keys("17186458316")
    driver.implicitly_wait(5)
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys("810925js")
    print("请输入验证码：")
    # 手动输入验证码
    security_code = input()
    time.sleep(1)
    driver.find_element_by_id("captcha_input").send_keys(security_code)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/main/div/div/div/div[1]/div/form/div[5]/div[2]/button').click()

    driver.implicitly_wait(5)
    # 加一个休眠，这样得到的cookie 才是登录后的cookie,否则可能打印的还是登录前的cookie
    time.sleep(5)
    cookiesAfter = driver.get_cookies() #获取所有的cookie


    for dic in cookiesAfter:    #找到名字为uid的字典，进行保存
        if dic['name']=='uid':
            with open('..\data\cookie.txt', 'w', encoding='utf-8') as f:
                f.write(json.dumps(dic))
                print(dic)

    driver.quit()
if __name__=='__main__':
    get_login_cookie()

