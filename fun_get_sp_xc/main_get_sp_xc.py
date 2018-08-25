import pandas as pd
from bs4 import BeautifulSoup
from numpy import nan as NaN
import re
def fun_time(data):
    #原始数据为 76’，去除最后‘，然后变成数字
    try:
        if data=='半':
            return ('半')
        if data=='-':
            return (NaN)
        else:
            # time=data[:-1]    #正常是好用的，有事不好用，所以用下面这个
            time=re.search('\d+',data).group(0)
            return (time)
    except:
        print('提取sp41数据中：时间出错，内容为：{}'.format(data))
def fun_socre(data):
    if data=='-':
        return (0,0)
    else:
        ls=[]
        ls=data.split(':')
        return (eval(ls[0]),eval(ls[1]))
def fun_z_k_s(data):
    if data=='-':
        return (NaN)
    else:
        return (eval(data))
def fun_biaodi(data):
    if ','in data:
        ls=data.split(',')
        value=(eval(ls[0])+eval(ls[1]))/2
        return (value)
    elif data=='-':
        return (NaN)
    else:
        return (eval(data))

#获取四和一数据：角球
def get_data_sp_corner(html_soup):
    corner=html_soup.select('#sp_corner > tr > td')
    ls_min = []
    ls_zd_goal = []
    ls_zd_p = []
    ls_corner = []
    ls_kd_goal = []
    ls_kd_p = []

    col = 0
    for st in corner:
        data = st.text.strip()
        if col % 6 == 0:  # 时间
            time = fun_time(data)
            ls_min.append(time)
        if col % 6 == 1:  # 比分
            ls_zd_goal.append(fun_socre(data)[0])
            ls_kd_goal.append(fun_socre(data)[1])
        if col % 6 == 2:  # 主水
            ls_zd_p.append(fun_z_k_s(data))
        if col % 6 == 3:  # 标的
            ls_corner.append(fun_biaodi(data))
        if col % 6 == 4:  # 客水
            ls_kd_p.append(fun_z_k_s(data))
        if col % 6 == 5:  # 日期
            pass
        col += 1

    dic = {'盘口_角球_时间': ls_min,
           '主_角球_球数': ls_zd_goal, '客_角球_球数': ls_kd_goal,
           '主_角球_水': ls_zd_p,
           '角球球': ls_corner,
           '客_角球_水': ls_kd_p}
    df = pd.DataFrame(dic, columns=['盘口_角球_时间', '主_角球_球数', '客_角球_球数', '主_角球_水', '角球球', '客_角球_水'])
    df = df.fillna(method='bfill')  # 使用后一个数据填充
    #df.to_excel('check_corner.xlsx')
    return (df)

#获取四和一数据：胜平负
def get_data_sp_bet(html_soup):
    bet=html_soup.select('#sp_bet > tr > td')
    ls_min = []
    ls_zd_goal = []
    ls_zd_p = []
    ls_bet = []
    ls_kd_goal = []
    ls_kd_p = []

    col = 0
    for st in bet:
        data = st.text.strip()
        if col % 6 == 0:  # 时间
            time = fun_time(data)
            ls_min.append(time)
        if col % 6 == 1:  # 比分
            ls_zd_goal.append(fun_socre(data)[0])
            ls_kd_goal.append(fun_socre(data)[1])
        if col % 6 == 2:  # 主水
            ls_zd_p.append(fun_z_k_s(data))
        if col % 6 == 3:  # 标的
            ls_bet.append(fun_biaodi(data))
        if col % 6 == 4:  # 客水
            ls_kd_p.append(fun_z_k_s(data))
        if col % 6 == 5:  # 日期
            pass
        col += 1

    dic = {'盘口_胜平负_时间': ls_min,
           '主_胜平负_球数': ls_zd_goal, '客_胜平负_球数': ls_kd_goal,
           '主_胜平负_水': ls_zd_p,
           '胜平负球': ls_bet,
           '客_胜平负_水': ls_kd_p}
    df = pd.DataFrame(dic, columns=['盘口_胜平负_时间', '主_胜平负_球数', '客_胜平负_球数', '主_胜平负_水', '胜平负球', '客_胜平负_水'])
    df = df.fillna(method='bfill')  # 使用后一个数据填充
    #df.to_excel('check_bet.xlsx')
    return (df)

#获取四和一数据：让分
def get_data_sp_rangfen(html_soup):
    rangfen=html_soup.select('#sp_rangfen > tr > td')
    ls_min=[]
    ls_zd_goal=[]
    ls_zd_p=[]
    ls_rangfen=[]
    ls_kd_goal=[]
    ls_kd_p=[]

    col=0
    for st in rangfen:
        data=st.text.strip()
        if col%6==0:    #时间
            time=fun_time(data)
            ls_min.append(time)
        if col%6==1:    #比分
            ls_zd_goal.append(fun_socre(data)[0])
            ls_kd_goal.append(fun_socre(data)[1])
        if col%6==2:    #主水
            ls_zd_p.append(fun_z_k_s(data))
        if col%6==3:    #标的
            ls_rangfen.append(fun_biaodi(data))
        if col%6==4:    #客水
            ls_kd_p.append(fun_z_k_s(data))
        if col%6==5:    #日期
            pass
        col+=1

    dic={'盘口_让分_时间':ls_min,
         '主_让分_球数':ls_zd_goal,'客_让分_球数':ls_kd_goal,
         '主_让分_水':ls_zd_p,
         '让分球':ls_rangfen,
         '客_让分_水':ls_kd_p}
    df=pd.DataFrame(dic,columns=['盘口_让分_时间','主_让分_球数','客_让分_球数','主_让分_水','让分球','客_让分_水'])
    df=df.fillna(method='bfill') #使用后一个数据填充
    #df.to_excel('check_rangfen.xlsx')
    return (df)

#获取四和一数据：大小球
def get_data_sp_daxiao(html_soup):
    daxiao=html_soup.select('#sp_daxiao > tr > td')
    ls_min=[]
    ls_zd_goal=[]
    ls_zd_p=[]
    ls_daxiao=[]
    ls_kd_goal=[]
    ls_kd_p=[]

    col=0
    for st in daxiao:
        data=st.text.strip()
        if col%6==0:    #时间
            ls_min.append(fun_time(data))
        if col%6==1:    #比分
            ls_zd_goal.append(fun_socre(data)[0])
            ls_kd_goal.append(fun_socre(data)[1])
        if col%6==2:    #主水
            ls_zd_p.append(fun_z_k_s(data))
        if col%6==3:    #标的
            ls_daxiao.append(fun_biaodi(data))
        if col%6==4:    #客水
            ls_kd_p.append(fun_z_k_s(data))
        if col%6==5:    #日期
            pass
        col+=1

    dic={'盘口_大小_时间':ls_min,
         '主_大小_球数':ls_zd_goal,'客_大小_球数':ls_kd_goal,
         '主_大小_水':ls_zd_p,
         '大小球':ls_daxiao,
         '客_大小_水':ls_kd_p}
    df=pd.DataFrame(dic,columns=['盘口_大小_时间','主_大小_球数','客_大小_球数','主_大小_水','大小球','客_大小_水'])
    df=df.fillna(method='bfill') #使用后一个数据填充
    # df.to_excel('check_daxiao.xlsx')
    return (df)

#提取现场数据
def _fun_data_tiqu_xc(ls_data):
    # ls_xc=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    ls_xc=list(map(lambda x:x.text,ls_data))
    num=len(ls_xc)
    error=0
    if num==20:
        pass
    elif num==16:
        ls_xc.insert(8,'50%')
        ls_xc.insert(8,'50%')
        ls_xc.append('50%')
        ls_xc.append('50%')
    else:
        for i in range(20):
            ls_xc.append('0')
            error=1
        ls_xc[8]=0.5
        ls_xc[9] = 0.5
        ls_xc[18] = 0.5
        ls_xc[19] = 0.5



    dic={'主_全_射正':ls_xc[0], '客_全_射正':ls_xc[1],
         '主_全_射偏':ls_xc[2],'客_全_射偏':ls_xc[3],
         '主_全_进攻':ls_xc[4], '客_全_进攻':ls_xc[5],
         '主_全_危险进攻':ls_xc[6],'客_全_危险进攻':ls_xc[7],
         '主_全_球权':ls_xc[8],'客_全_球权':ls_xc[9],
         '主_半_射正': ls_xc[10], '客_半_射正': ls_xc[11],
         '主_半_射偏': ls_xc[12], '客_半_射偏': ls_xc[13],
         '主_半_进攻': ls_xc[14], '客_半_进攻': ls_xc[15],
         '主_半_危险进攻': ls_xc[16], '客_半_危险进攻': ls_xc[17],
         '主_半_球权': ls_xc[18], '客_半_球权': ls_xc[19]
         }

    return (dic,error)

def __fun_tiqu_time_num(info_str):

    ls_info = info_str.strip().split('-')
    time_min = ls_info[0][:-2]
    num_temp = ls_info[1]
    num_goal = re.search('\d+', num_temp).group(0)
    return (time_min,num_goal)

def _fun_data_tiqu_log(logs):
    ls_goal_num=[]
    ls_goal_time=[]
    ls_corner_num=[]
    ls_corner_time=[]
    ls_yc_num=[]
    ls_yc_time=[]
    ls_rc_time=[]
    ls_rc_num=[]
    tianqi=''
    changdi=[]

    for i in logs:
        # print(i.text.strip())
        try:
            bo=i.find(attrs={'src':"/assets/images/event/hg.png"})  #主队进球图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_goal_num.append(num)
                ls_goal_time.append(time)
        except:
            pass
        try:
            bo = i.find(attrs={'src': "/assets/images/event/gg.png"})  # 客队进球图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_goal_num.append(num)
                ls_goal_time.append(time)
        except:
            pass

        try:
            bo = i.find(attrs={'src': "/assets/images/event/hc.png"})  # 主队角球图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_corner_num.append(num)
                ls_corner_time.append(time)
        except:
            pass
        try:
            bo = i.find(attrs={'src': "/assets/images/event/gc.png"})  # 客队角球图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_corner_num.append(num)
                ls_corner_time.append(time)
        except:
            pass

        try:
            bo = i.find(attrs={'src': "/assets/images/event/hyc.png"})  # 主队黄牌图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_yc_num.append(num)
                ls_yc_time.append(time)
        except:
            pass
        try:
            bo = i.find(attrs={'src': "/assets/images/event/gyc.png"})  # 客队黄牌图标
            if bo:
                time,num=__fun_tiqu_time_num(i.text)
                ls_yc_num.append(num)
                ls_yc_time.append(time)
        except:
            pass

        try:
            bo = i.find(attrs={'src': "/assets/images/event/hrc.png"})  # 主队红牌图标
            if bo:
                time, num = __fun_tiqu_time_num(i.text)
                ls_rc_num.append(num)
                ls_rc_time.append(time)
        except:
            pass
        try:
            bo = i.find(attrs={'src': "/assets/images/event/grc.png"})  # 客队红牌图标
            if bo:
                time, num = __fun_tiqu_time_num(i.text)
                ls_rc_num.append(num)
                ls_rc_time.append(time)
        except:
            pass

            try:
                bo = i.find(attrs={'src': "/assets/images/event/tq.png"})  # 天气图标
                if bo:
                    tianqi=i.text.strip()
            except:
                pass

        try:
            bo = i.find(attrs={'src': "/assets/images/event/cd.png"})  # 场地图标
            if bo:
                changdi=i.text.strip()
        except:
            pass

    goal_time=','.join(ls_goal_time)
    goal_num=','.join(ls_goal_num)
    corner_time=','.join(ls_corner_time)
    corner_num = ','.join(ls_corner_num)
    yc_time=','.join(ls_yc_time)
    yc_num = ','.join(ls_yc_num)
    rc_time=','.join(ls_rc_time)
    rc_num = ','.join(ls_rc_num)

    dic={'进球时间':goal_time,'进球数量和':goal_num,
         '角球时间':corner_time,'角球数量和':corner_num,
         '黄牌时间':yc_time,'黄牌数量和':yc_time,
         '红牌时间':rc_time,'红牌数量和':rc_num,
         '天气情况':tianqi,'场地情况':changdi,
         }
    return (dic)

#提取现场数据，通过html,当前被使用的函数
def fun_main_get_data_xc(html_soup):
    # 获取半场和全场两个时间点的射偏射正，进攻，球权等信息
    data_xc_nums = html_soup.select('#race_data_pct > div.panel-body > div > div > div.small-2')
    dic_she_jin,error=_fun_data_tiqu_xc(data_xc_nums)

    #读取时间记录中数据
    data_xc_logs=html_soup.select('#race_events > li.bullet-item')
    dic_log=_fun_data_tiqu_log(data_xc_logs)
    dic={}  #新建一个空字典
    dic.update(dic_she_jin)
    dic.update(dic_log)
    sr=pd.Series(dic)
    return (sr,error)

def fun_main_get_data_sp(html_soup):
    # 获取四张表的数据
    df_rangfen = get_data_sp_rangfen(html_soup)
    df_daxiao = get_data_sp_daxiao(html_soup)
    df_bet = get_data_sp_bet(html_soup)
    df_corner = get_data_sp_corner(html_soup)
    # 调整索引为时间，便于下面的合并
    df_daxiao = df_daxiao.set_index('盘口_大小_时间')
    df_rangfen = df_rangfen.set_index('盘口_让分_时间')
    df_corner = df_corner.set_index('盘口_角球_时间')
    df_bet = df_bet.set_index('盘口_胜平负_时间')
    # 合并四张表的数据
    df_tmp1 = pd.merge(df_daxiao, df_rangfen, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df_corner, df_bet, how='outer', left_index=True, right_index=True)
    df = pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    ############################################
    #应该先对表进行排序，
    df.sort_values(by=['主_大小_球数','客_大小_球数'],inplace=True)
    # 对合并后的总表进行处理
    df = df.loc[~df.index.duplicated(keep='last')]  # 时间去重，只保留第一个
    df.drop(['主_让分_球数', '客_让分_球数', '主_胜平负_球数', '客_胜平负_球数'], axis=1, inplace=True)  # 去掉这些重复的比赛比分

    df['比赛时间'] = df.index  # 把时间索引变回成 比赛时间的列
    #####################################################
    #重大bug，比赛时间为NaN的是初盘的时间，有两个半，出现，其实有一个半是初盘
    #因为NaN 是 时间为- 的数据  还有些比赛没有‘半’时间标签
    df.dropna(subset=['比赛时间'],inplace=True)
    #####################################################
    df = df.fillna(method='pad')  # 向下填充，空白区域，要重新赋值，这里要重新赋值，才能显示出来

    return (df)

if __name__=='__main__':
    df=pd.DataFrame()
    with open('temp.html', 'rb') as f1:
        html=f1.read()
    html_soup=BeautifulSoup(html,'lxml')
    df=fun_main_get_data_sp(html_soup)
    print(df)

