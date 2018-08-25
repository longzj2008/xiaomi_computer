#!/usr/bin/env python
# -*- coding:utf-8 -*-
import itchat
import pandas as pd
from fun_time import time_fun

def wechat_send(content,num,ls_username):

    try:
        # itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
        time_mark = time_fun.time_now().strftime('%Y-%m-%d %H:%M:%S')
        ###################################################################
        #对聊天记录存储
        with open('data\\wechat_record.txt', 'a+', encoding='utf-8') as f:
            f.write(time_mark+'&&')
            f.write(content+'\n')
        path_check='data\\'+str(num)+'.txt'
        with open(path_check,'w',encoding='utf-8') as f1:
            f1.write(time_mark+'&&')
            f1.write(content+'\n')
        #发送到微信
        for username in ls_username:
            try:
                itchat.send_msg(msg=time_mark, toUserName=username)
                itchat.send_msg(msg=content, toUserName=username)
            except:
                pass
    except:
        print('微信发送出错')
        pass

    pass

if __name__=='__main__':
    # itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录

    dic={'比赛':['1','2'],'人数':[3,4]}
    df=pd.DataFrame(dic)
    info=df.to_json(orient='index',force_ascii=False)
    wechat_send(info)







