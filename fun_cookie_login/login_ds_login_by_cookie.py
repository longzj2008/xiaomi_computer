#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from selenium import webdriver
import json

#用于测试，使用是注意读取cookie的路径
def login_by_cookie():

    driver = webdriver.Chrome()
    driver.get("https://www.dszuqiu.com/race_sp/492501")
    # 方案 1：手动添加Cookie
    # driver.add_cookie({'name':'uid','value':'R-240430-fcc080a705b2daeba051ad'})

    #方案 2：读取cookie.txt添加Cookie
    # 注意：读取cookie值，移植时注意文件路径要更改
    with open(r'..\data\cookie.txt', 'r', encoding='utf-8') as f:
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
if __name__=='__main__':
    driver=login_by_cookie()
    url = 'https://www.dszuqiu.com/diary/20180611'
    driver.get(url)