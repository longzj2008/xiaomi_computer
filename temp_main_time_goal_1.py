#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import re
import time
from fun_time import time_fun
from fun_make_table import make_sp_xc_table
from main_01_01_download_data_now import fun_download_game_trace
from main_02_00_compress_data import  main_compress_data_for_now



def fun_find_time_sp(df_input,path_read_folder):
    # df_input.reset_index(drop=False, inplace=True)  # df_input 已经在上一步的download中重置过了
    df_tmp=pd.DataFrame()
    path=''
    ls_abnormal_id=[]
    for id in df_input['本场比赛ID']:  # 每一个id获取生成一个序列
        df_single = df_input[df_input['本场比赛ID'] == id]
        df_single['主_进1_时间'].replace(150,99,inplace=True)
        df_single['客_进1_时间'].replace(150,99,inplace=True)
        ls_goal_1_zd_time = df_single['主_进1_时间']
        ls_goal_1_kd_time = df_single['客_进1_时间']
        ################################################################################################################
        # 从 ds_data_sp41 中提取每一个id的sp数据
        ###############################################################################################################
        # 对提取到的xc数据进行整理，生成一个表格
        ls_file_names=os.listdir(path_read_folder + 'ds_data_sp41\\')
        for file_name in ls_file_names:
            if str(id) in file_name:
                path = path_read_folder + 'ds_data_sp41\\' + file_name
                break
        if path=='':
            path='找不到本场比赛sp相关数据'
            print(path)

        else:
            print('读取文件：{}'.format(path))

        df_sp,abnormal_id=make_sp_xc_table.make_sp_table(path)
        ls_abnormal_id.append(abnormal_id)
        ###########################################################################################################
        #提取当前比赛时间点的数据
        if not df_sp.empty:
            df_sp_time_zd = df_sp[df_sp['比赛时间'].isin(ls_goal_1_zd_time)]
            df_sp_time_zd.reset_index(drop=False,inplace=True)
            df_sp_time_kd = df_sp[df_sp['比赛时间'].isin(ls_goal_1_kd_time)]
            df_sp_time_kd.reset_index(drop=False, inplace=True)
        else:
            df_sp_time_zd=pd.DataFrame()
            df_sp_time_kd = pd.DataFrame()
        df_end_tmp=pd.merge(df_sp_time_zd,df_sp_time_kd,left_index=True,right_index=True,how='outer')
        df_tmp=df_tmp.append(df_end_tmp)
    #重置索引，便于后面进行合并
    df_tmp.reset_index(drop=False,inplace=True)
    df_output=df_tmp.copy()

    return (df_output,ls_abnormal_id)

def fun_find_time_xc(df_input,path_read_folder):

    # df_input.reset_index(drop=False, inplace=True)  # df_input 已经在上一步的download中重置过了
    df_tmp=pd.DataFrame()
    ls_abnormal_id=[]
    path=''
    for id in df_input['本场比赛ID']:  # 每一个id获取生成一个序列
        df_single = df_input[df_input['本场比赛ID'] == id]

        df_single['主_进1_时间'].replace(150,99,inplace=True)
        df_single['客_进1_时间'].replace(150, 99,inplace=True)
        ls_goal_1_zd_time = df_single['主_进1_时间']
        ls_goal_1_kd_time = df_single['客_进1_时间']
        ################################################################################################################
        # 从 ds_data_xctable中提取每一个id的sp数据
        ###############################################################################################################
        #对提取到的xc数据进行整理，生成一个表格
        ls_file_names=os.listdir(path_read_folder + 'ds_data_xc_table\\')
        for file_name in ls_file_names:
            if str(id) in file_name:
                path = path_read_folder + 'ds_data_xc_table\\' + file_name
                break
        if path=='':
            path='找不到本场比赛xc_table相关数据'
            print(path)
        else:
            print('读取文件：{}'.format(path))

        # 对提取到的xc数据进行整理，生成一个表格
        df_xc_table,abnormal_id=make_sp_xc_table.make_xc_table(path)
        ls_abnormal_id.append(abnormal_id)
        ###########################################################################################################
        ###########################################################################################################
        #提取当前比赛时间点的数据
        # print('#2')
        # print(df_xc_table)
        # print(df_xc_table['时间'])
        # print(ls_goal_1_zd_time)
        # print(ls_goal_1_kd_time)
        if not df_xc_table.empty:
            df_xc_table_time_zd = df_xc_table[df_xc_table['时间'].isin(ls_goal_1_zd_time)]
            df_xc_table_time_zd.reset_index(drop=False,inplace=True)
            df_xc_table_time_kd = df_xc_table[df_xc_table['时间'].isin(ls_goal_1_kd_time)]
            df_xc_table_time_kd.reset_index(drop=False, inplace=True)
        else:
            df_xc_table_time_zd=pd.DataFrame()
            df_xc_table_time_kd = pd.DataFrame()
        df_end_tmp=pd.merge(df_xc_table_time_zd,df_xc_table_time_kd,left_index=True,right_index=True,how='outer')
        df_tmp=df_tmp.append(df_end_tmp)
    df_tmp.reset_index(drop=False, inplace=True)
    df_output=df_tmp
    return (df_output,ls_abnormal_id)


def main_goal_1_data(path_prefix,save_path):
    file_path=path_prefix+'\\'+'ds_data'
    ls=os.listdir(file_path)
    df=pd.DataFrame()
    ls_empty_id = []

    for id_data_name in ls:     #读取包含一页id的列表
        ###############################################################################################################
        #从 ds_data 中提取每一个日期中的ID 信息，及半场，全场的数据
        ###############################################################################################################
        path=path_prefix+'\\'+'ds_data'+'\\'+id_data_name
        print(path)
        try:
            df_tmp=pd.read_csv(path)    #使用'utf-8'尝试读取
        except:
            df_tmp = pd.read_csv(path,encoding='gbk')
        # print(df_tmp.columns.values.tolist())     #打印df的列名

        #读取到原始的csv文件后，赋值给df_id_nwe,以前是进行调整后，赋值
        df_id_new=df_tmp
        df_id_new.reset_index(drop=False, inplace=True)
        ###############################################################################################################
        #进入到每一个ID内部，开始提取到，所有需要的xc，sp 页数据，
        df_sp_need,ls_abnormal_sp_id=fun_find_time_sp(df_id_new,path_prefix)
        df_xc_table_need,ls_abnormal_xc_id=fun_find_time_xc(df_id_new,path_prefix)
        ###############################################################################################################
        #把有问题的id 列表连接起来
        ls_empty_id.extend(ls_abnormal_sp_id)
        ls_empty_id.extend(ls_abnormal_xc_id)
        #合并三张表
        df_tmp=pd.merge(df_sp_need,df_xc_table_need,left_index=True,right_index=True,how='outer')

        df_end=pd.merge(df_id_new,df_tmp,left_index=True,right_index=True,how='outer')

        df=df.append(df_end)

    ###############################################################################################################
    #对最终得到的df，进行最终的筛选，保存
    ###############################################################################################################
    df.to_excel(save_path)
    return (df)


if __name__=='__main__':
    pass
    # 需要更多地方，根据要生成的数据
    ls_files_test = ['football_data\\test\\']
    for prefix in ls_files_test:
        # prefix 是数据所在路径，
        save_name ='goal_1' +'_'+prefix.split('\\')[-1]+'.xlsx'  # 代表文件夹名字
        save_path = prefix + save_name
        print(save_path)
        main_goal_1_data(prefix,save_path)
