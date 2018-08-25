#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
import numpy as np
import time
from fun_time import time_fun
from numpy import nan as NaN
import re
from fun_make_table import make_sp_xc_table


def fun_qiuquan(x):
    num=re.search('\d+',x).group(0)
    n=eval(num)/100
    return (n)
def fun_time_min(x):
    print(type(x))
    print(x)
    n=eval(x)/60
    print(n)
    return (n)

def __fun_generate_sr(df,ls_min):

    ls_index=list(df.index)
    ls_col=list(df.columns)
    # ls_col_new_name=[]
    sr=pd.Series()
    i=0
    for inde in ls_index:
        sr1=df.ix[inde,]    #索引出 df 的每一行，每行代表的是一个时间点
        ls_new_index=[]
        ls_value=sr1.tolist()   #返回每行的值

        for c in ls_col:
            tmp=ls_min[i]+c
            ls_new_index.append(tmp)    #保证生成的索引，是一致的，虽然索引的可能是第16分钟，但是标签仍是15分钟
        i += 1

        sr2=pd.Series(ls_value,index=ls_new_index)
        sr=sr.append(sr2)   #注意每次要重新赋值

    return (sr)

def _fun_get_sp41_min(df_sp,ls_min):
    df=pd.DataFrame()
    for min in ls_min:
        min_int=eval(min)
        df_tmp=df_sp[df_sp['比赛时间']==min_int]
        df=df.append(df_tmp,ignore_index=True)
    return (df)

def _fun_get_xc_table_min(df_xc_table,ls_min):
    df=pd.DataFrame()
    for min in ls_min:
        min_int=eval(min)
        df_tmp=df_xc_table[df_xc_table['时间']==min_int]
        df=df.append(df_tmp,ignore_index=True)
    return (df)

def _fun_add_fator_base_xc(df):
    #注意在clean_data中 ‘inf’会被变成 15
    df['主_射正_数量'] = df['主_射正_数量'].replace(0, 0.1)  # 
    df['客_射正_数量'] = df['客_射正_数量'].replace(0, 0.1)  # 
    df['主_射偏_数量'] = df['主_射偏_数量'].replace(0, 0.3)  # 3次射正，没有射偏，则3/0.3=10
    df['客_射偏_数量'] = df['客_射偏_数量'].replace(0, 0.3)  # 3次射正，没有射偏，则3/0.3=10
    

    df['主_射正偏和'] = df['主_射正_数量'] + df['主_射偏_数量']
    df['主_射正偏和比危险进攻']=df['主_射正偏和']/df['主_危险进攻_数量']

    df['主_进球比射正']=df['主_进球_数量']/df['主_射正_数量']
    df['主_进球比射正偏和']=df['主_进球_数量']/df['主_射正偏和']
    df['主_进球比危险进攻']=df['主_进球_数量']/df['主_危险进攻_数量']
    
    
    df['主_射正比射偏'] = df['主_射正_数量'] / df['主_射偏_数量']
    df['主_射正比危险进攻']=df['主_射正_数量']/df['主_危险进攻_数量']

    df['主_危险进攻比进攻']=df['主_危险进攻_数量']/df['主_进攻_数量']

    df['主_射正比时间'] = df['主_射正_数量'] / df['时间'] * 60
    df['主_射偏比时间'] = df['主_射偏_数量'] / df['时间'] * 60
    df['主_射正偏和比时间']=df['主_射正偏和']/df['时间']*60
    df['主_危险进攻比时间']=df['主_危险进攻_数量']/df['时间']*60
    df['主_进攻比时间'] = df['主_进攻_数量'] / df['时间'] * 60
###################################################################################
    df['客_射正偏和'] = df['客_射正_数量'] + df['客_射偏_数量']
    df['客_射正偏和比危险进攻'] = df['客_射正偏和'] / df['客_危险进攻_数量']

    df['客_进球比射正'] = df['客_进球_数量'] / df['客_射正_数量']
    df['客_进球比射正偏和'] = df['客_进球_数量'] / df['客_射正偏和']
    df['客_进球比危险进攻'] = df['客_进球_数量'] / df['客_危险进攻_数量']


    df['客_射正比射偏'] = df['客_射正_数量'] / df['客_射偏_数量']
    df['客_射正比危险进攻'] = df['客_射正_数量'] / df['客_危险进攻_数量']

    df['客_危险进攻比进攻'] = df['客_危险进攻_数量'] / df['客_进攻_数量']

    df['客_射正比时间'] = df['客_射正_数量'] / df['时间'] * 60
    df['客_射偏比时间'] = df['客_射偏_数量'] / df['时间'] * 60
    df['客_射正偏和比时间'] = df['客_射正偏和'] / df['时间'] * 60
    df['客_危险进攻比时间'] = df['客_危险进攻_数量'] / df['时间'] * 60
    df['客_进攻比时间'] = df['客_进攻_数量'] / df['时间'] * 60
    
###################################################################################
    #主客关系
    df['主_危险进攻比客_危险进攻']=df['主_危险进攻_数量']/df['客_危险进攻_数量']
    df['主_射正比客_射正']=df['主_射正_数量']/df['客_射正_数量']
    df['主_射偏比客_射偏'] = df['主_射偏_数量'] / df['客_射偏_数量']
    df['主_射正偏和比客_射正偏和']=df['主_射正偏和']/df['客_射正偏和']

    return (df)

def _fun_add_fator_base_sp(df):
    df['sp跨值']=df['大小球']-df['主_大小_球数']-df['客_大小_球数']

    return (df)
    pass

def fun_save_log(log):
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    log_detail=time_now+':'+log+'\n'
    with open('data\\Errorlog.txt', 'a+', encoding='utf-8') as f:
        f.write(log_detail)
    print(log)

def duplicated_varnames(df):
    """Return a dict of all variable names that
    are duplicated in a given dataframe."""
    repeat_dict = {}
    var_list = list(df) # list of varnames as strings
    for varname in var_list:
        # make a list of all instances of that varname
        test_list = [v for v in var_list if v == varname]
        # if more than one instance, report duplications in repeat_dict
        if len(test_list) > 1:
            repeat_dict[varname] = len(test_list)
    return (repeat_dict)

def main_compress_data(ls_min,path_prefix,save_path):
    file_path=path_prefix+'\\'+'ds_data'
    ls=os.listdir(file_path)
    df=pd.DataFrame()
    ls_empty_id = []
    ########################
    #公共变量的设置,当有增加时，需要更改
    ls_sp41_columns = ['主_大小_球数', '客_大小_球数', '主_大小_水', '大小球', '客_大小_水',
                     '主_让分_水', '让分球', '客_让分_水',
                     '主_角球_球数', '客_角球_球数', '主_角球_水', '角球球', '客_角球_水',
                     '主_胜平负_水', '胜平负球', '客_胜平负_水', '比赛时间', 'sp跨值']
    ls_xc_table_columns=['时间', '主_角球_数量', '客_角球_数量', '主_射正_数量', '客_射正_数量',
                         '主_进球_数量', '客_进球_数量', '主_射偏_数量', '客_射偏_数量',
                         '主_危险进攻_数量', '客_危险进攻_数量', '主_进攻_数量', '客_进攻_数量',
                         '主_射正偏和', '主_射正偏和比危险进攻', '主_进球比射正',
                         '主_进球比危险进攻','主_进球比射正偏和', '主_射正比射偏', '主_射正比危险进攻', '主_危险进攻比进攻',
                         '主_射正比时间', '主_射偏比时间', '主_射正偏和比时间', '主_危险进攻比时间',
                         '主_进攻比时间', '客_射正偏和', '客_射正偏和比危险进攻', '客_进球比射正',
                         '客_进球比危险进攻', '客_进球比射正偏和','客_射正比射偏', '客_射正比危险进攻', '客_危险进攻比进攻',
                         '客_射正比时间', '客_射偏比时间', '客_射正偏和比时间', '客_危险进攻比时间',
                         '客_进攻比时间', '主_危险进攻比客_危险进攻', '主_射正比客_射正', '主_射偏比客_射偏',
                         '主_射正偏和比客_射正偏和']

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
        #进入到每一个ID内部，开始提取xc，sp 页数据，
        #这两页的数据，xc中一部分数据直接连接到id页数据中
        #sp页数据和xc数据的表格部分，分别生成dataframe后，放入文件夹中单独存储，需要使用时，需要结合提取的时间，抽取生成数据
        df_sp_new=pd.DataFrame()
        df_xc_table_new=pd.DataFrame()

        for id in df_id_new['本场比赛ID']:     #每一个id获取生成一个序列
        ################################################################################################################
        #从 ds_data_sp41 中提取每一个id的sp数据
        ###############################################################################################################
            path=path_prefix+'\\'+'ds_data_sp41\\'+id_data_name[:-4]+'_'+str(id)+'.csv'
            print(path)
            try:
                # 去除数据中包含的文字，以100作为半场的代码时间
                df_sp,abnormal_id=make_sp_xc_table.make_sp_table(path)
                #提取对应时间的数据:
                df_tmp_01=_fun_get_sp41_min(df_sp,ls_min)
                df_tmp=_fun_add_fator_base_sp(df_tmp_01)
                ###############################################
                #这里需要reindex一下，以便确保所有的列名一致，且按相同的顺序
                df_tmp=df_tmp.reindex(columns=ls_sp41_columns)

                if df_tmp.empty:
                    ls_empty_id.append(id)
                #对数据进行初步整理，然后压缩成一个序列
                sr = __fun_generate_sr(df_tmp, ls_min)
            except:
                sr=pd.Series()
                ls_empty_id.append(id)
                log='提取SP41数据出错，使用空序列填充，ID为：{}'.format(id)
                fun_save_log(log)
            #把得到的序列生成一个df

            df_sp_new=df_sp_new.append(sr,ignore_index=True)    #所有的id生成一个列表


        ############################################################################################################
        #从 ds_data_xc_table 中提取每一个id的xc_table数据
        ############################################################################################################
            path=path_prefix+'\\'+'ds_data_xc_table\\'+id_data_name[:-4]+'_'+str(id)+'.csv'
            print(path)
            # 读取文件,生成df_xc_table
            try:
                #读取现场table，并对表格进行填充，处理
                df_xc_table,abnormal_id = make_sp_xc_table.make_xc_table(path)
                # 提取对应时间的数据:
                df_tmp_01 = _fun_get_xc_table_min(df_xc_table, ls_min)
                #增加几个基础因子
                df_tmp=_fun_add_fator_base_xc(df_tmp_01)
                ##################################################################
                #这里需要reindex一下，以便确保所有的列名一致，且按相同的顺序
                df_tmp=df_tmp.reindex(columns=ls_xc_table_columns)

                if df_tmp.empty:

                    ls_empty_id.append(id)
                sr=__fun_generate_sr(df_tmp,ls_min)

            except:
                sr=pd.Series()
                ls_empty_id.append(id)
                # log='提取xc_table数据出错，使用空序列填充，ID为：{}'.format(id)
                # fun_save_log(log)
            df_xc_table_new = df_xc_table_new.append(sr, ignore_index=True)  # 所有的id生成一个列表


    ###################################################################################################################
    #把从3个文件夹提取到的信息 合并到一个df中
    ###############################################################################################################
        df_id_sp=pd.concat([df_id_new, df_sp_new], axis=1)
        # df_id_sp.to_excel('id_sp.xlsx')
        df_id_sp_xc=pd.concat([df_id_sp,df_xc_table_new],axis=1)
        # df_id_sp_xc.to_excel('id_sp_xc.xlsx')
        df=df.append(df_id_sp_xc,ignore_index=True)
    # df.to_excel('df.xlsx')

    ###############################################################################################################
    #对最终得到的df，进行最终的筛选，保存
    ###############################################################################################################
    ##save_path 有变量传入
    ###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #删除xc数据为空，sp41 数据为空的行
    print(ls_empty_id)
    ls_empty_id=list(set(ls_empty_id))
    print('这些是需要删除的问题比赛{}'.format(ls_empty_id))
    if len(ls_empty_id)>0:
        for id_del in ls_empty_id:
            df = df[df['本场比赛ID'] != id_del]
    print('压缩后的数据存放路径：{}'.format(save_path))
    df.to_excel(save_path)

    return (df)

def main_compress_data_for_now(path_read):

    ################################################################
    # 设定取样的时间点
    ################################################################
    ls_min = []
    for i in range(1, 101):
        if i % 5 == 0:
            ls_min.append(str(i))
    print(ls_min)

    ################################################################
    # 需要更多地方，根据要生成的数据
    ls_files_test = []
    ls_files_test.append(path_read)
    ################################################################
    for prefix in ls_files_test:
        print(prefix)
        save_name=prefix.split('\\')[1]
        save_path=prefix+save_name+'.xlsx'
        df=main_compress_data(ls_min, prefix,save_path)

        #因为now里面没有关于半场，全场的数据
        #主_半_比分,客_半_比分,主_全_比分,客_全_比分,主_半_角球,客_半_角球,主_全_角球,客_全_角球
        # 100这个特殊时间，代表半场sp数据，但是有的数据没有半，所以为了统一性，统一取50分钟数据；
        df['主_半_比分']=df['50主_大小_球数']
        df['客_半_比分']=df['50客_大小_球数']
        df['主_全_比分']=df['95主_大小_球数']
        df['客_全_比分']=df['95客_大小_球数']
        df['主_半_角球']=df['50主_角球_球数']
        df['客_半_角球']=df['50客_角球_球数']
        df['主_全_角球']=df['95主_角球_球数']
        df['客_全_角球']=df['95客_角球_球数']


        df.to_excel(save_path)
        return (df)

if __name__=='__main__':
    # print('开始生成数据')
    time_start=time_fun.time_now()
    ################################################################
    #设定取样的时间点
    ################################################################
    ls_min = []
    for i in range(1,101):  #一定要到101，把100分钟包含进去，100分钟代表半场数据
        if i%5==0:
            ls_min.append(str(i))
    print(ls_min)

    ################################################################
    #手动指定要压缩的原始数据
    # # ls_files_train=['football_data\\01','football_data\\02']
    # ls_files_train=['football_data\\03']
    # for prefix in ls_files_train:
    #     main_compress_data(ls_min,prefix)
    ################################################################
    #需要更多地方，根据要生成的数据
    ls_files_test=['football_data\\test01']
    # ls_files_test = ['football_data\\now']

    ################################################################
    for prefix in ls_files_test:

        #prefix 是数据所在路径，
        #测试用，生成data_now.xlsx, 真实在跟踪比赛，下载的叫now。xlsx
        save_name='data'+'_'+prefix[14:]+'.xlsx'    #代表文件夹名字
        save_path=prefix+'\\'+save_name
        main_compress_data(ls_min, prefix,save_path)
    ################################################################
    # ls_files_now=['football_data\\now']
    # for prefix in ls_files_now:
    #     main_compress_data(ls_min, prefix)


    time_end=time_fun.time_now()
    yongshi=time_end-time_start
    print('生成训练数据：完成,用时{}'.format(yongshi))

###########################################################################
#对now 相关进行测试
    # path_read= 'football_data\\now\\'
    # main_compress_data_for_now(path_read)
    # #













