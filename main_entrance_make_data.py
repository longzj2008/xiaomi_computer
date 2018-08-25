#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
import main_02_00_compress_data
import main_02_01_clean_data
import main_02_02_make_model_data as mmd
import main_03_train
import main_04_query
import main_05_manual_analyse
from fun_time import time_fun
from fun_make_table import make_sp_xc_table

#####################################################################################
print('开始生成数据')
#开始计时
#####################################################################################
time_start = time_fun.time_now()
print(('开始时间为：{}'.format(time_start)))

####################################################################################
#处理 bug 关于sp原始数据的最后一个，清除掉
# ls_data=['01','02','03','04','05','test','trace']
# num=0
# for name in ls_data:
#     path='football_data\\'+name+'\\ds_data_sp41'
#     ls_files=os.listdir(path)
#     for file in ls_files:
#         path_file=path+'\\'+file
#         try:
#             try:
#                 df=pd.read_csv(path_file,encoding='gbk')
#             except:
#                 df = pd.read_csv(path_file,encoding='utf-8')
#
#             df.dropna(subset=['Unnamed: 0'], inplace=True)
#             df.to_csv(path_file)
#         except:
#             print('{}出错'.format(path_file))
#
#         print(num)
#         num=num+1

################################################################
# 设定取样的时间点
################################################################
ls_min = []
for i in range(1, 101):  # 一定要到101，把100分钟包含进去，100分钟代表半场数据
    if i % 5 == 0:
        ls_min.append(str(i))
print(ls_min)
#####################################################################################
#压缩数据
#####################################################################################
# ls_compress=['football_data\\01','football_data\\02','football_data\\03','football_data\\04',
#                    'football_data\\05','football_data\\06','football_data\\test']
# for prefix in ls_compress:
#     # prefix 是数据所在路径，
#     # 测试用，生成data_now.xlsx, 真实在跟踪比赛，下载的叫now。xlsx
#     save_name = 'data' + '_' + prefix[14:] + '.xlsx'  # 代表文件夹名字
#     save_path = prefix + '\\' + save_name
#     main_02_00_compress_data.main_compress_data(ls_min, prefix, save_path)

#####################################################################################
#清洗数据
#####################################################################################

#ls_clean=['football_data\\01','football_data\\02','football_data\\03','football_data\\04','football_data\\05',
#            'football_data\\06'
 #                       ]
# ls_clean=['football_data\\test']
# print('#'*40)
# print('开始清洗数据')
# for path in ls_clean:
#     print('清洗的路径：{}'.format(path))
#     main_02_01_clean_data.main_clean_data(path)

#####################################################################################
#生成模型
#####################################################################################
# #生成基础3个模型
# print('#'*40)
#
print('开始生成基础模型：2')
mmd.main_make_model_2_sp() #没有参数，是多所有的数据文件进行操作
#
# #
# #     ###################################################################
# #     #生成子模型，参数说明
# #     #file_name=''   等于空时对data_all 中所有的xlsx 进行生成， 写指定的文件名，对指定文件名进行生成
# #     #model_base 基于那个基础模型生成
# #     #model_save+path 生成后的模型保存在哪里
# #     #target_name 在base模型中生成，采用多少分钟的进球和做为筛选
# #     #target_more 进球和 大于
# #     #target_less 进球和 小于
# #     ###################################################################
# # # print('开始生成子模型：1')
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_0', '30球和', 0, 0.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_0_1', '30球和', 0, 1.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_0_2', '30球和', 0, 2.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_0_3', '30球和', 0, 3.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_1', '30球和', 0.5, 1.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_2', '30球和', 1.5, 2.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_3', '30球和', 2.5, 3.5)
# # # mmd.main_make_sub_model('', 'model_1', 'model_1_4', '30球和', 3.5, 10.5)
# # # print('开始生成子模型：2')
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_0', '半球和', 0, 0.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_0_1', '半球和', 0, 1.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_0_2', '半球和', 0, 2.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_0_3', '半球和', 0, 3.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_0_4', '半球和', 0, 4.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_1', '半球和', 0.5, 1.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_1_2', '半球和', 0.5, 2.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_1_3', '半球和', 0.5, 3.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_1_4', '半球和', 0.5, 4.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_2', '半球和', 1.5, 2.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_3', '半球和', 2.5, 3.5)
# # # mmd.main_make_sub_model('', 'model_2', 'model_2_4', '半球和', 3.5, 10.5)
# # # print('开始生成子模型：2_sp')
# # # mmd.main_make_sub_model('', 'model_2_sp', 'model_2_sp_0_2', '半sp跨值', 0, 2.15)
# # # mmd.main_make_sub_model('', 'model_2_sp', 'model_2_sp_1', '半sp跨值', 0, 1.15)
# # # mmd.main_make_sub_model('', 'model_2_sp', 'model_2_sp_1.5_5', '半sp跨值', 1.35, 5.15)
# # # mmd.main_make_sub_model('', 'model_2_sp', 'model_2_sp_1_2', '半sp跨值', 0.85, 2.15)
# # # mmd.main_make_sub_model('', 'model_2_sp', 'model_2_sp_2', '半sp跨值', 2.15, 8)
# #
# # #####################################################################################
# # #训练模型
# # #####################################################################################
# # #模型model：1的列名长度为236
# # #模型mode2：的列名长度为350
# # #####################################
# # lenth=0
# # # ls_models=['model_1','model_1_0','model_1_0_1','model_1_0_2','model_1_0_3','model_1_1','model_1_2','model_1_3','model_1_4',
# # #            'model_2','model_2_0','model_2_0_1','model_2_0_2','model_2_0_3','model_2_0_4','model_2_1','model_2_1_2','model_2_1_3',
# # #            'model_2_1_4','model_2_2','model_2_3','model_2_4',
# # #            'model_2_sp','model_2_sp_0_2','model_2_sp_1','model_2_sp_1','model_2_sp_1.5_5','model_2_sp_1_2','model_2_sp_2'
# # #            ]
#
# ls_models=['model_2_sp']
# ######################################
#
# for model_name in ls_models:
#     print('#' * 30)
#     print('测试模型 {}'.format(model_name))
#     if 'model_2' in model_name:
#         lenth=409-7
#     elif 'model_1'in model_name:
#         lenth=236-5
#     else:
#         print('错:{}'.format(model_name))
#         break
#     main_03_train.main_train(model_name,lenth)
# #
# # #####################################################################################
# # #查询模型
# # #####################################################################################
# file_name='test'    #其实是文件名中包括
# for model_name in ls_models:
#     print('#'*30)
#     print('测试模型 {},测试文件为：{}'.format(model_name,file_name))
#     if 'model_2' in model_name:
#         lenth = 409 - 7
#     elif 'model_1' in model_name:
#         lenth = 236 - 5
#     else:
#         print('错:{}'.format(model_name))
#         lenth=0
#         break
#     main_04_query.main_query_model(file_name,model_name,lenth)
#
#
#
# #####################################################################################
# #单独检验模型
# #####################################################################################
#
# main_05_manual_analyse.main_analyse(ls_models)

#####################################################################################
#结束时间计时
#####################################################################################
time_end=time_fun.time_now()
yongshi=time_end-time_start
print('生成训练数据：完成,用时{}'.format(yongshi))