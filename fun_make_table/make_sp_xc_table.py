#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
def delete_ban(df):
    pass

    return (df)

def fun_adjust_sp(df):
    # 新增一个，对比赛时间靠后，但进球却变小的删除
    df.sort_values(by=['比赛时间'], inplace=True)
    # print(df[['比赛时间','主_大小_球数','客_大小_球数']])
    arr_zd=np.array(df['主_大小_球数'])
    arr_kd=np.array(df['客_大小_球数'])
    zd=np.gradient(arr_zd)
    # print(zd)
    kd=np.gradient(arr_kd)
    i=0
    num_z=101
    for z in zd:
        if z<0:
            num_z=i
            break
        i+=1
    i=0
    num_k=101
    for k in kd:
        if k<0:
            num_k=i
            break
        i+=1
    #取小，截取
    if num_z>num_k:
        num=num_k
    else:
        num=num_z
    df=df[df['比赛时间']<=(num+1)]
    # print(df[['比赛时间', '主_大小_球数', '客_大小_球数']])
    return (df)


def make_sp_table(path):
    # 读取文件,生成df_sp
    file_name_id=''

    try:
        df_sp_orginal = pd.read_csv(path, index_col=0)
    except:
        df_sp_orginal = pd.read_csv(path, encoding='gbk', index_col=0)



    try:
        # 去除数据中包含的文字，以100作为半场的代码时间
        ls_time=list(df_sp_orginal['比赛时间'])

        df_sp_orginal = df_sp_orginal.replace('半', '100')  # 特殊的标记100，代表半场sp

        # xc_table中比赛比赛时间的数据，下载后，存储为了int,目的是为了填充比赛时间
        df_sp_orginal['比赛时间'] = df_sp_orginal['比赛时间'].astype(int)
        ############################################################
        #修理数据，处理有异常的数据, 根据梯度，进行修正
        df_sp_orginal=fun_adjust_sp(df_sp_orginal)
        ################################################################
        # 生成一个包含每一分钟的比赛时间列
        df_time = pd.DataFrame({'比赛时间': list(range(1, 101))})  # 从1分钟到100分钟
        # 将比赛时间列与表合并，方式为交集，根据比赛时间合并，填充所有比赛时间
        df_sp = pd.merge(df_sp_orginal, df_time, left_on='比赛时间', right_on='比赛时间', how='outer')
        # 对生成的df，按比赛时间进行排序
        df_sp = df_sp.sort_values(by=['比赛时间', '主_大小_球数', '客_大小_球数'])  # 从小到大排序，优先级按列表中内容

        # 进行去重操作
        df_sp.drop_duplicates(subset=['比赛时间'], keep='last', inplace=True)

        # 向下填充数据
        df_sp = df_sp.fillna(method='pad')  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来

        # 对于首行数据为空的，再次填充为0
        df_sp = df_sp.fillna(0)  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来

        ####################################################
        df_sp.reset_index(inplace=True)
        ls_col=['主_大小_球数', '客_大小_球数', '主_大小_水', '大小球', '客_大小_水', '主_让分_水',
                '让分球', '客_让分_水', '主_角球_球数', '客_角球_球数', '主_角球_水',
                '角球球', '客_角球_水', '主_胜平负_水', '胜平负球', '客_胜平负_水', '比赛时间']
        df_sp=df_sp.reindex(columns=ls_col)
        #####################################################
        #对让分球 去绝对值
        #####################################################
        df_sp['让分球']=df_sp['让分球'].apply(lambda x:abs(x))

    except:
        print('生成sp table 出错！')
        print(path)
        file_name_id=path.split('\\')[-1].replace('.csv','').split('_')[-1]
        df_sp=pd.DataFrame()

    return (df_sp,file_name_id)


def make_xc_table(path):

    file_name_id=''
    try:
        df_xc_table_orginal = pd.read_csv(path)
    except:
        df_xc_table_orginal = pd.read_csv(path, encoding='gbk')

    try:
        # xc_table中比赛时间的数据，下载后，存储为了int,目的是为了填充时间
        df_xc_table_orginal['时间'] = df_xc_table_orginal['时间'].astype(int)
        # 生成一个包含每一分钟的时间列
        df_time = pd.DataFrame({'时间': list(range(1, 101))})  # 从1分钟到100分钟
        # 将时间列与表合并，方式为交集，根据时间合并，填充所有时间
        df_xc_table = pd.merge(df_xc_table_orginal, df_time, left_on='时间', right_on='时间', how='outer')
        # 对生成的df，按时间进行排序
        df_xc_table = df_xc_table.sort_values(by='时间')
        # 进行去重操作,除去出现合并后，重复的时间
        df_xc_table.drop_duplicates(subset=['时间'], keep='last', inplace=True)
        # 向下填充数据
        df_xc_table = df_xc_table.fillna(method='pad')  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来
        # 对于首行数据为空的，再次填充为0
        df_xc_table = df_xc_table.fillna(0)  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来
    except:
        print('生成xc table 出错！')
        print(path)
        file_name_id=path.split('\\')[-1].replace('.csv','').split('_')[-1]
        df_xc_table=pd.DataFrame()
    return (df_xc_table,file_name_id)

def make_score_table(df):

    try:
        # 生成一个包含每一激发量的区间dataframe，从0.01到0.99
        ls_jifa=[]
        for i in range(100):
            ls_jifa.append(i/100)
        df_time = pd.DataFrame({'激发量_值': ls_jifa})  # 激发量的值从0到0.99
        # 将时间列与表合并，方式为交集，根据激发量_值合并，填充所有激发量_值
        df_xc_table = pd.merge(df, df_time, left_on='激发量_值', right_on='激发量_值', how='outer')
        # 对生成的df，按激发量_值进行排序
        df_xc_table = df_xc_table.sort_values(by='激发量_值')
        # 进行去重操作,除去出现合并后，重复的时间
        df_xc_table.drop_duplicates(subset=['激发量_值'], keep='last', inplace=True)
        # 向下填充数据
        df_xc_table = df_xc_table.fillna(method='pad')  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来
        # 对于首行数据为空的，再次填充为0
        df_xc_table = df_xc_table.fillna(0)  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来
        df_xc_table.reset_index(inplace=True)
    except:
        print('生成socre 表格 出错！')
        df_xc_table = pd.DataFrame()

    return (df_xc_table)

    pass

if __name__=='__main__':
    #path='20180701p2_493541.csv'
    path='20180701_495101.csv'
    path = '20180701p2_494873.csv'
    # path = '20180701p2_494903.csv'
    df,id=make_sp_table(path)

    df.to_excel('111.xlsx')
    # print(df['主_大小_球数'])