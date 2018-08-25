import pandas as pd
import numpy as np
import os
import re

def ___fun_compare(x):
    #比值大于15的全部变成15
    if x>14.9:
        x=14.9
    return (x)
    pass

def __fun_03_adjust_value(df):
    #本场比赛ID	联赛名称	主_名字	客_名'
    df_tmp_storge=df[['本场比赛ID','联赛名称','主_名字','客_名字']]
    del df['本场比赛ID']
    del df['联赛名称']
    del df['主_名字']
    del df['客_名字']
    try:
        df=df.astype('float')
    except:
        print('转换类型时出错，请人工检查！')
        df.to_excel('check.xlsx')
    df['初盘_让球_绝对值']=df['初盘_让球'].apply(lambda x:abs(x))
    ls_columns=list(df.columns)
    for column  in ls_columns:
        if bool(re.search(r'\d+时间',column)):
            #时间 列除以60
            df[column]=df[column]/60
        #处理比值
        if bool(re.search(r'比',column)):
            #相除大于15的，都按15算
            df[column]=df[column].apply(___fun_compare)

        elif bool(re.search(r'进攻',column)):
            # 进攻，危险进攻 列除以20
            df[column] = df[column] / 20
        elif bool(re.search(r'让分',column)) and (not bool(re.search(r'水',column))):
            # 让分，放大2倍，在压缩环节，制作sp41表格时，已经把让分调整为绝对值
            df[column] = df[column]*2
        elif bool(re.search(r'角球_球数', column)):
            # 角球 列除以2
            df[column] = df[column] / 2
        elif bool(re.search(r'射偏_数量', column)):
            # 射偏 列除以2
            df[column] = df[column] / 2
        elif bool(re.search(r'射正_数量', column)):
            # 射正 列除以2
            df[column] = df[column] / 2
        elif bool(re.search(r'射正偏和', column)):
            if not bool(re.search(r'比', column)):
                # 射正偏和 /4
                df[column] = df[column] / 4
        elif bool(re.search(r'水', column)):
            # 删除85分钟后水
            try:
                min=re.search(r'\d+',column).group()
                if eval(min)>=80:
                    del df[column]
            except:
                pass
    #经过上述处理后，数值的最大，最小值范围在 -5~10 之间，下面的用于确认
    df_des=df.describe()
    # df_des.to_excel('describe.xlsx')
    #把合并后输出
    df_end=pd.concat([df_tmp_storge, df], axis=1)
    return (df_end)

def __fun_02_del_str(df,s='友谊'):
    # df=df.astype('str')
    # df.to_excel('111.xlsx')
    df1=df[df['联赛名称'].str.contains(s)]
    ls_id=list(df1['本场比赛ID'])
    for id in ls_id:
        df=df[df['本场比赛ID']!=id]
    return (df)

def __fun_01_filter_columns(df):
    df_orginal=df
    ls_columns_orginal = list(df_orginal.columns)

    #####################################################
    # 获取不包含数字列 和包含数字列
    ls_id = []
    ls_sp_xc_time = []
    ls_sp_daxiao_pankou = []
    ls_sp_daxiao_shui = []
    ls_sp_daxiao_kuazhi=[]
    ls_sp_rangfen_pankou = []
    ls_sp_rangfen_shui = []
    ls_sp_goal = []
    ls_sp_corner = []
    ls_xc_all_4 = []
    ls_others = []
    for column in ls_columns_orginal:
        if bool(re.search(r'\d', column)):
            if '时间' in column:
                if bool(re.search(r'\d+时间',column)):
                    ls_sp_xc_time.append(column)
            elif '大小球' in column:
                ls_sp_daxiao_pankou.append(column)
            elif '大小_水' in column:
                ls_sp_daxiao_shui.append(column)
            elif '跨值' in column:
                ls_sp_daxiao_kuazhi.append((column))
            elif '让分球' in column:
                ls_sp_rangfen_pankou.append(column)
            elif '让分_水' in column:
                ls_sp_rangfen_shui.append(column)
            elif ('进攻' in column) or ('危险进攻' in column) or ('射正' in column) or ('射偏' in column):
                ls_xc_all_4.append(column)
            elif '大小_球数' in column:
                ls_sp_goal.append(column)
            elif '角球_球数' in column:
                ls_sp_corner.append(column)
            else:
                ls_others.append(column)
        else:
            ls_id.append(column)
    #print('剔除的数据项点：{}'.format(ls_others))#包含角球，胜平负的水，以及从xc中提取到时进球和角球数量
    # # #############sp
    # # print(ls_sp_corner)
    # # print(ls_sp_goal)
    # # print(ls_sp_rangfen_pankou)
    # # print(ls_sp_rangfen_shui)
    # print(ls_sp_daxiao_pankou)
    # # print(ls_sp_daxiao_shui)
    # # #############xc
    # # print(ls_xc_all_4)
    # print(ls_sp_xc_time)
    # # #############id
    # # print(ls_id)
    ls_id_useful = ['本场比赛ID', '联赛名称', '主_名字', '客_名字', '初盘_让球', '初盘_大小', '主_半_比分', '客_半_比分', '主_全_比分', '客_全_比分']
    # print(ls_id_useful)
    ####################################################
    ##筛选出需要使用的数据
    ls_columns_01_filter = []
    ls_columns_01_filter.extend(ls_id_useful)
    ls_columns_01_filter.extend(ls_sp_xc_time)
    ls_columns_01_filter.extend(ls_sp_goal)
    ls_columns_01_filter.extend(ls_sp_corner)
    ls_columns_01_filter.extend(ls_sp_daxiao_pankou)
    ls_columns_01_filter.extend(ls_sp_daxiao_shui)
    ls_columns_01_filter.extend(ls_sp_daxiao_kuazhi)
    ls_columns_01_filter.extend(ls_sp_rangfen_pankou)
    ls_columns_01_filter.extend(ls_sp_rangfen_shui)
    ls_columns_01_filter.extend(ls_xc_all_4)
    ##01_fliter: 对列名进行切片
    df_01_filter = df_orginal.reindex(columns=ls_columns_01_filter)
    ##02_ 对0，空进行处理

    return (df_01_filter)

#adjust:对最终得到df ，进行最好的筛选
def _fun_adjust_all(df):
    df=df.astype('str')
    ###00 对列名进行切片筛选
    print('开始对列名进行切片筛选')
    df=__fun_01_filter_columns(df)
    # print(list(df.columns))
    ###01 删除友谊赛
    print('删除友谊赛')
    df=__fun_02_del_str(df,'友谊')   #删除联赛名称中包含友谊的比赛，友谊赛目标不明确，所以删除
    ###03 去零和空
    print('去除 0 和 空')
    df = df.replace(np.inf, np.nan)
    df=df.replace('inf','15')   #inf 为最大
    df=df.replace('-','0.01')
    df=df.replace('0','0.01')     #把数据中0，变为0.01
    df=df.replace('0.0','0.01')
    df = df.replace('nan', '0.01')
    ###02 调整数字范围，到-5~15
    print('把值调整到-5~15内')
    df=__fun_03_adjust_value(df)

    return (df)

def main_clean_data(path_read):
    #####################################################################################
    # 需要更改的地方
    ls_paths_wait_deal = []
    ls_paths_wait_deal.append(path_read)
    #####################################################################################
    ls_paths_xlsx = []  # 文件夹下要处理的xlsx文件
    # 找到文件夹下要处理的xlsx文件
    for ls_path_wait_deal in ls_paths_wait_deal:
        ls_tmp = os.listdir(ls_path_wait_deal)
        for name in ls_tmp:
            if '.xlsx' in name:
                xx = ls_path_wait_deal + '\\' + name
                ls_paths_xlsx.append(xx)
    print(ls_paths_xlsx)

    # 对找到excel文件中的列名进行第一次初步筛选
    for ls_path_xlsx in ls_paths_xlsx:
        df_orginal = pd.read_excel(ls_path_xlsx)  # df_orginal, 只是把3种数据压缩在一起的一个df
        df_all = _fun_adjust_all(df_orginal)  # 去除不需要的列，填充数据，同时调整数据的范围到-5~15
        file_name = ls_path_xlsx.split('\\')[-1]
        path_data_train = 'ds_data_train' + '\\' + 'data_all' + '\\' + file_name
        print('clean_data后数据存放到：{}'.format(path_data_train))
        df_all.to_excel(path_data_train)
    return (df_all)


if __name__=='__main__':
    #####################################################################################
    #需要更改的地方
    #把需要进行清理的文件夹名字列出
    # ls_paths_wait_deal=['football_data\\01','football_data\\02',
    #                     'football_data\\03','football_data\\04','football_data\\05',
    #                     'football_data\\test',
    #                     ]
    # ls_paths_wait_deal=[
    #                     'football_data\\test',
    #                     ]
    ls_paths_wait_deal = ['football_data\\test']
    #####################################################################################
    for path in ls_paths_wait_deal:
        main_clean_data(path)





