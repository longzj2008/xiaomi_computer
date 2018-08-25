import pandas as pd
import os
import re
from fun_time import time_fun
import time

# #########################################################################################################################
# #生成模型 一 相关
# #########################################################################################################################
# def _fun_target_model_1_cal(x):
#     if x>2.5:   #代表3球以上
#         x=3
#     elif x>1.5 :  #代表2球
#         x=2
#     elif x>0.5:
#         x=1
#     else:
#         x=0
#     return (x)
# #注意：
# ###在clean 数据中，对进攻和危险进攻，是除以20， 对射正，射偏是除以2，对时间是除以60，对85分钟后水，删除
# def fun_make_model_1(df):
#     #目标：判断30分钟~半场结束是否可以买小； 目标=半场球和-30分钟球和
#     #条件：不做筛选，
#     #清理：保留时间小于等于30分钟的攻防数据
#
#     ####################################################
#     #生成目标
#     df['半球和']=df['主_半_比分']+df['客_半_比分']
#     df['30球和']=df['30主_大小_球数']+df['30客_大小_球数']
#     df['目标']=df['半球和']-df['30球和']
#     df['目标']=df['目标'].apply(_fun_target_model_1_cal)
#
#     ####################################################
#     #切片，去除不需要的列
#     ls_columns=list(df.columns)
#     # print(ls_columns)
#     ls_01=['本场比赛ID', '联赛名称', '主_名字', '客_名字','目标', '初盘_让球', '初盘_大小']
#     ls_02=[]
#     for column in ls_columns:
#         #筛选出时间小于50的
#         try:
#             min=re.search(r'\d+',column).group()
#             if eval(min)<=30:
#                 ls_02.append(column)
#         except:
#             pass
#     ls_columns_model_1=[]
#     ls_columns_model_1.extend(ls_01)
#     ls_columns_model_1.extend(ls_02)
#     df_end=df.reindex(columns=ls_columns_model_1)
#
#     return (df_end)
#     #模型1 在30分钟时进行判断
# def main_make_model_1(file_name=''):
#     ####################################
#     # 需要修改的地方，当生成模型数据时
#     path_train = 'ds_data_train'
#     model_name = 'model_1'
#
#     # 开始遍历训练用数据，生成模型数据
#     ls_xlsxs = os.listdir(path_train + '\\' + 'data_all')
#     ####################################################
#     #通过下面的判断，默认对data_all 中的所有表进行生产模型，如果输入文件名，那么只对数据的名字进行处理
#     ls_xlsxs_final=[]
#     if file_name=='':
#         ls_xlsxs_final=ls_xlsxs
#     else:
#         for name in ls_xlsxs:
#             if file_name in name:
#                 ls_xlsxs_final.append(name)
#     print('需要生成模型1的有{}'.format(ls_xlsxs_final))
#     for xlsx in ls_xlsxs_final:
#         print(xlsx)
#         ##################################################################
#         path_read_data = path_train + '\\' + 'data_all' + '\\' + xlsx
#         df_orginal = pd.read_excel(path_read_data)
#         ##################################################################
#         # 生成模型一：
#         df_model_1 = fun_make_model_1(df_orginal)
#         ##################################################################
#         lenth_col = len(list(df_model_1.columns))
#         print('模型model：1的列名长度为{}'.format(lenth_col))
#         if df_model_1.empty:
#             print('符合模型1 要求的比赛为：空')
#             df_state = False
#         else:
#             df_state = True
#         ##################################################################
#         ################################################################
#         path_model_1_save_data = path_train + '\\' + model_name + '\\' + xlsx
#         ################################################################
#         print('model_1生成完毕后，保存路径为：{}'.format(path_model_1_save_data))
#         df_model_1.to_excel(path_model_1_save_data)
#     #返回的df_state 适用于最后一个
#     return (df_state)

#########################################################################################################################
#生成模型 二 sp 相关
#model_2代表 进行半场判断，sp代表对水位值的判断
###在clean 数据中，对进攻和危险进攻，是除以20， 对射正，射偏是除以2，对时间是除以60，对85分钟后水，删除
################################################################################################################
#目标1: 改为： 0 代表 0个进球； 1代表1~2个，2代表2~3个，3代表3个以上
def _fun_target_model_2_cal_sp(x):
    if x>2.5:   #代表3球以上
        x=3
    elif x>1.5 and x<3.5 :  #代表2球
        x=2
    elif x>0.5 and x<2.5:
        x=1
    elif x<1.5:
        x=0
    return (x)

def fun_make_model_2_sp(df):
    #目标：判断30分钟~半场结束是否可以买小； 目标=半场球和-30分钟球和
    #条件：不做筛选，
    #清理：保留时间小于等于30分钟的攻防数据
    ####################################################
    #生成目标，半球和以 50分钟的数据为准
    df['半球和']=df['50主_大小_球数']+df['50客_大小_球数']
    df['全球和']=df['95主_大小_球数']+df['95客_大小_球数']
    df['半sp跨值']=df['50大小球']-df['半球和']  #100大小球代表半场大小球数据，取消了，因为有些比赛没有半
    df['目标']=df['全球和']-df['半球和']
    df['目标']=df['目标'].apply(_fun_target_model_2_cal_sp)

    ####################################################
    #切片，去除不需要的列
    ls_columns=list(df.columns)
    # print(ls_columns)
    ls_01=['本场比赛ID', '联赛名称', '主_名字', '半sp跨值','初盘_让球','全球和','目标', '初盘_大小','半球和']
    ls_02=[]
    for column in ls_columns:
        #筛选出时间小于等于50的
        try:
            min=re.search(r'\d+',column).group()
            if eval(min)<=50:
                ls_02.append(column)
        except:
            pass
    ls_columns_model_2=[]
    ls_columns_model_2.extend(ls_01)
    ls_columns_model_2.extend(ls_02)
    # print('test'+'$'*20)
    # print(len(ls_columns_model_2))
    # print(ls_columns_model_2)
    # print('test'+'$'*20)
    df_end=df.reindex(columns=ls_columns_model_2)

    return (df_end)

#模型2 在45分钟时进行判断
def main_make_model_2_sp(file_name=''):
    ####################################
    # 需要修改的地方，当生成模型数据时
    path_train = 'ds_data_train'
    model_name = 'model_2_sp'

    # 开始遍历训练用数据，生成模型数据
    ls_xlsxs = os.listdir(path_train + '\\' + 'data_all')

    ####################################################
    #通过下面的判断，默认对data_all 中的所有表进行生产模型，如果输入文件名，那么只对数据的名字进行处理
    ls_xlsxs_final=[]
    if file_name=='':
        ls_xlsxs_final=ls_xlsxs
    else:
        for name in ls_xlsxs:
            if file_name in name:
                ls_xlsxs_final.append(name)
    print('需要生成模型2_sp的有{}'.format(ls_xlsxs_final))
    for xlsx in ls_xlsxs_final:
        print(xlsx)
        ##################################################################
        path_read_data = path_train + '\\' + 'data_all' + '\\' + xlsx
        df_orginal = pd.read_excel(path_read_data)
        ##################################################################
        # 生成模型二：
        df_model_2 = fun_make_model_2_sp(df_orginal)
        ##################################################################
        lenth_col = len(list(df_model_2.columns))
        print('模型model2：的列名长度为{}'.format(lenth_col))
        if df_model_2.empty:
            print('符合模型2 要求的比赛为：空')
            df_state = False
        else:
            df_state = True
        ##################################################################
        ################################################################
        path_model_2_save_data = path_train + '\\' + model_name + '\\' + xlsx
        ################################################################
        print('model_2生成完毕后，保存路径为：{}'.format(path_model_2_save_data))
        df_model_2.to_excel(path_model_2_save_data)
    #返回的df_state 适用于最后一个
    return (df_state)

##################################################
#目标1: 改为： 0 代表 0-1个进球； 1代表0~2个，2代表1~3个，3代表2~4个
def _fun_target_model_2_cal_sp_t_1(x):
    if x>1.5:   #代表3球以上
        x=3
    elif x>0.5 and x<3.5 :  #代表2球
        x=2
    elif x<2.5:
        x=1
    elif x<1.5:
        x=0
    return (x)

def fun_make_model_2_sp_t_1(df):

    del df['目标']
    ###################################################
    #基于model_2_sp， 重新生成目标
    df['目标']=df['全球和']-df['半球和']
    df['目标']=df['目标'].apply(_fun_target_model_2_cal_sp_t_1)

    ####################################################
    #切片，去除不需要的列
    ls_columns=list(df.columns)
    # print(ls_columns)
    ls_01=['本场比赛ID', '联赛名称', '主_名字', '半sp跨值','初盘_让球','全球和','目标', '初盘_大小','半球和']
    ls_02=[]
    for column in ls_columns:
        #筛选出时间小于等于50的
        try:
            min=re.search(r'\d+',column).group()
            if eval(min)<=50:
                ls_02.append(column)
        except:
            pass
    ls_columns_model_2=[]
    ls_columns_model_2.extend(ls_01)
    ls_columns_model_2.extend(ls_02)

    df_end=df.reindex(columns=ls_columns_model_2)

    return (df_end)

def main_make_model_2_sp_t_1_base_model(model_name_base = 'model_2_sp',model_name_new = 'model_2_sp_t_1'):
    ####################################
    # 需要修改的地方，当生成模型数据时
    path_folder='ds_data_train\\'

    # 开始遍历训练用数据，生成模型数据
    ls_xlsxs = os.listdir(path_folder + model_name_base)

    for xlsx in ls_xlsxs:
        ##################################################################
        path_read_data = path_folder+model_name_base+'\\'+xlsx
        print('需要生成的xlsx有{}'.format(path_read_data))
        df_orginal = pd.read_excel(path_read_data)
        ##################################################################
        # 生成模型二：
        df_model_2 = fun_make_model_2_sp_t_1(df_orginal)
        ##################################################################
        lenth_col = len(list(df_model_2.columns))
        print('模型{}：的列名长度为{}'.format(model_name_new,lenth_col))
        if df_model_2.empty:
            print('符合模型{} 要求的比赛为：空'.format(model_name_new))
            df_state = False
        else:
            df_state = True
    #     ##################################################################
    #     ################################################################
        path_model_2_save_data = path_folder+model_name_new+'\\'+xlsx
        ################################################################
        print('模型生成完毕后，保存路径为：{}'.format(path_model_2_save_data))
        df_model_2.to_excel(path_model_2_save_data)
    #返回的df_state 适用于最后一个
    return (df_state)

#########################################################################################################################
#生成子模型 的通用函数
#########################################################################################################################
##下面的基础模型的分支，df=df[(df['30球和']<1.5)] 小于等于1个
def main_make_sub_model(file_name='',model_base='model_1',model_name_save='model_1_0_1',target_name='30球和',target_more=0,target_less=5):
    ####################################################
    # 需要修改的地方，当生成模型数据时
    path_train = 'ds_data_train'
    model_name_read = model_base
         #这里是要修改的地方
    # 开始遍历训练用数据，生成模型数据
    ls_xlsxs = os.listdir(path_train + '\\' + model_name_read)
    ####################################################
    #通过下面的判断，默认对data_all 中的所有表进行生产模型，如果输入文件名，那么只对数据的名字进行处理
    ls_xlsxs_final=[]
    if file_name=='':
        ls_xlsxs_final=ls_xlsxs
    else:
        for name in ls_xlsxs:
            if file_name in name:
                ls_xlsxs_final.append(name)
    ####################################################
    for xlsx in ls_xlsxs_final:
        print(xlsx)
        path_read_data=path_train + '\\' + model_name_read+'\\'+xlsx
        df=pd.read_excel(path_read_data)
        #######################################################################
        ###在clean 数据中，对进攻和危险进攻，是除以20， 对射正，射偏是除以2，对时间是除以60，对85分钟后水，删除
        #以下为筛选df的条件
        print('{}的“{}”：筛选的范围为{}：{}'.format(model_name_save,target_name,target_more,target_less))
        df=df[(df[target_name]>target_more)&(df[target_name]<target_less)]

        #######################################################################
        lenth_col = len(list(df.columns))
        print('模型{}的列名长度为{}'.format(model_name_save,lenth_col))
        if df.empty:
            print('符合模型{} 要求的比赛为：空'.format(model_name_save))
            df_state=False
        else:
            df_state=True
            #######################################################################
        #以下为保存数据
        path_save_data=path_train + '\\' + model_name_save+'\\'+xlsx
        print('{}生成后，保存路径为：{}'.format(model_name_save,path_save_data))
        df.to_excel(path_save_data)
    return (df_state)


if __name__=='__main__':
    pass
    main_make_model_2_sp('test')
    #main_make_model_2_sp_t_1_base_model('model_2_sp','model_2_sp_t_1')
    # main_make_sub_model('', 'model_2_sp', 'model_2_sp_1', '半sp跨值', 0, 1.15)
    # main_make_sub_model('', 'model_2_sp', 'model_2_sp_1_2', '半sp跨值', 0.95, 2.15)
    # main_make_sub_model('', 'model_2_sp', 'model_2_sp_2', '半sp跨值', 1.9, 8)
    # main_make_sub_model('', 'model_2_sp', 'model_2_sp_1.5_5', '半sp跨值', 1.4, 5)
    ###################################################################
    #file_name=''   等于空时对data_all 中所有的xlsx 进行生成， 写指定的文件名，对指定文件名进行生成
    #model_base 基于那个基础模型生成
    #model_save+path 生成后的模型保存在哪里
    #target_name 在base模型中生成，采用多少分钟的进球和做为筛选
    #target_more 进球和 大于
    #target_less 进球和 小于
    ###################################################################
    # main_make_model_1('')
    # main_make_sub_model('', 'model_1', 'model_1_0', '30球和', 0, 0.5)
    # main_make_sub_model('', 'model_1', 'model_1_0_1', '30球和', 0, 1.5)
    # main_make_sub_model('', 'model_1', 'model_1_0_2', '30球和', 0, 2.5)
    #begiin
    # main_make_sub_model('test', 'model_1', 'model_1_0_3', '30球和', 0, 3.5)
    # main_make_sub_model('', 'model_1', 'model_1_1', '30球和', 0.5, 1.5)
    # main_make_sub_model('', 'model_1', 'model_1_2', '30球和', 1.5, 2.5)
    # main_make_sub_model('', 'model_1', 'model_1_3', '30球和', 2.5, 3.5)
    # main_make_sub_model('', 'model_1', 'model_1_4', '30球和', 3.5, 10.5)


    # main_make_model_2('')
    # #main_make_sub_model(file_name='',model_base='model_1',model_name_save='model_1_0_3',target_name='30球和',target_more=0,target_less=3.5)

#    main_make_sub_model('', 'model_2', 'model_2_0', '半球和', 0, 0.5)
#    main_make_sub_model('', 'model_2', 'model_2_0_1', '半球和', 0, 1.5)
#    main_make_sub_model('', 'model_2', 'model_2_0_2', '半球和', 0, 2.5)
#    main_make_sub_model('', 'model_2', 'model_2_0_3', '半球和', 0, 3.5)
#    main_make_sub_model('', 'model_2', 'model_2_1', '半球和', 0.5, 1.5)
#    main_make_sub_model('', 'model_2', 'model_2_1_2', '半球和', 0.5, 2.5)
#    main_make_sub_model('', 'model_2', 'model_2_1_3', '半球和', 0.5, 3.5)
#    main_make_sub_model('', 'model_2', 'model_2_2', '半球和', 1.5, 2.5)
#    main_make_sub_model('', 'model_2', 'model_2_3', '半球和', 2.5, 3.5)
#    main_make_sub_model('', 'model_2', 'model_2_4', '半球和', 3.5, 10.5)
#     main_make_sub_model('', 'model_2', 'model_2_0_4', '半球和', 0, 4.5)
#     main_make_sub_model('', 'model_2', 'model_2_1_4', '半球和', 0.5, 4.5)
