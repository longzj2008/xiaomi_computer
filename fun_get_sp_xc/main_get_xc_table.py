import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from numpy import nan as NaN
import re


def _fun_get_orginal_data(html_soup,selector='#highcharts-0 > svg > g '):
    data=html_soup.select(selector)
    #0 4 8 12

    ls_y_value=[]
    ls_y_label=[]
    ls_x_value=[]
    ls_x_label=[]

    ls_zd_xy_value=[]
    ls_kd_xy_value=[]

    ls_zd_goal_x_value=[]
    ls_kd_goal_x_value=[]
    ls_zd_corner_x_value=[]
    ls_kd_corner_x_value=[]

    for i in data:
        class_name=i.get('class')

        # #print(class_name)
        # # #print(i.text)
        if class_name==['highcharts-grid']:
            if len(i.find_all('path')):
                ls_tmp = []
                for m in i.find_all('path'):
                    ls_tmp=m.get('d').split(' ')
                    ls_y_value.append(float(ls_tmp[-1].strip()))
            ##print(ls_y_value)

        if class_name == ['highcharts-axis']:
            if len(i.find_all('path')):
                ls_tmp = []
                for m in i.find_all('path'):
                    # #print(m)
                    ls_tmp=m.get('d').split(' ')
                    ls_x_value.append(float(ls_tmp[1].strip()))
                ls_x_value=ls_x_value[:-1]  #去掉最后一个，最后一个为重新画线
            #print(ls_x_value)

        if class_name == ['highcharts-axis-labels', 'highcharts-xaxis-labels']:
            ls_tmp=i.find_all('text')
            for m in ls_tmp:
                ls_x_label.append(int(m.text.strip()))
            #print(ls_x_label)


        if class_name == ['highcharts-axis-labels', 'highcharts-yaxis-labels']:
            ls_tmp=i.find_all('text')
            for m in ls_tmp:
                ls_y_label.append(int( m.text.strip()))
            ##print(ls_y_label)

        if class_name == ['highcharts-series-group']:
            # #print(i)
            #print(i.find_all('path'))
            for m in i.find_all('path'):
                # #print(m)
                # #print(m.get('stroke'))

                if m.get('stroke')=='#E45050':  # 主队的颜色为红色
                    # #print(m)
                    zd=m.get('d')
                    ls_xy_str=zd[1:].split('L')
                    for xy in ls_xy_str:
                        ls_tmp=xy.strip().split(' ')
                        ls_tmp2=[]
                        for xxyy in ls_tmp:
                            ls_tmp2.append(float(xxyy))
                        ls_zd_xy_value.append(ls_tmp2)
                    #print(ls_zd_xy_value)


                if m.get('stroke')=='#10AF80':  # 主队的颜色为红色
                    kd=m.get('d')
                    ls_xy_str=kd[1:].split('L')
                    for xy in ls_xy_str:
                        ls_tmp=xy.strip().split(' ')
                        ls_tmp2=[]
                        for xxyy in ls_tmp:
                            ls_tmp2.append(float(xxyy))
                        ls_kd_xy_value.append(ls_tmp2)
                    ##print(ls_kd_xy_value)

            for n in i.find_all('image'):
                if n.get('fill')=='#E45050':
                    if n.get('xlink:href')=='/assets/images/icon_goal20x20.png':    #代表进球图标
                        x_value=n.get('x')
                        ls_zd_goal_x_value.append(float(x_value))
                    elif n.get('xlink:href')=='/assets/images/icon_corner14x14.png':    #代表角球图标
                        x_value=n.get('x')
                        ls_zd_corner_x_value.append(float(x_value))

                elif n.get('fill')=='#10AF80':
                    if n.get('xlink:href') == '/assets/images/icon_goal20x20.png':  # 代表进球图标
                        x_value = n.get('x')
                        ls_kd_goal_x_value.append(float(x_value))
                    elif n.get('xlink:href') == '/assets/images/icon_corner14x14.png':  # 代表角球图标
                        x_value = n.get('x')
                        ls_kd_corner_x_value.append(float(x_value))

    #应对时间轴(x轴)中不是以0开始，而是以10开始的
    #调整成以0开始，主要用于偏移



    #时间轴x运算
    value_per_min=(ls_x_value[-1]-ls_x_value[0])/(ls_x_label[-1]-ls_x_label[0])
    value_per_cishu=(ls_y_value[-1]-ls_y_value[0])/(ls_y_label[-1]-ls_y_label[0])
    #主队xy运算
    arr_zd_xy = np.array(ls_zd_xy_value)
    arr_zd_xy[:, 0] = (arr_zd_xy[:, 0] - arr_zd_xy[0][0])/value_per_min+1   #加1 做了1分钟偏移
    arr_zd_xy[:, 0]=np.round(arr_zd_xy[:, 0])
    arr_zd_xy[:, 1] = abs((arr_zd_xy[:, 1] - arr_zd_xy[0][1])/value_per_cishu)
    arr_zd_xy[:, 1]=np.round(arr_zd_xy[:, 1] )
    #print('###'*100)
    # #print(arr_zd_xy)
    ls_zd_xy_value=arr_zd_xy.tolist()

    #客队xy运算
    arr_kd_xy = np.array(ls_kd_xy_value)
    arr_kd_xy[:, 0] = (arr_kd_xy[:, 0] - arr_kd_xy[0][0])/value_per_min+1   #加1 做了1分钟偏移
    arr_kd_xy[:, 0]=np.round(arr_kd_xy[:, 0])
    arr_kd_xy[:, 1] = abs( (arr_kd_xy[:, 1] - arr_kd_xy[0][1])/value_per_cishu)
    arr_kd_xy[:, 1]=np.round(arr_kd_xy[:, 1] )
    #print('###'*100)
    ls_kd_xy_value=arr_kd_xy.tolist()
 
    #主队进球时间
    #print('###'*100)
    arr_zd_goal=np.array(ls_zd_goal_x_value)
    arr_zd_goal=np.round( arr_zd_goal/value_per_min)+1
    ls_zd_goal_x_value=arr_zd_goal.tolist()
    #客队进球时间
    #print('###'*100)
    arr_kd_goal=np.array(ls_kd_goal_x_value)
    arr_kd_goal=np.round( arr_kd_goal/value_per_min)+1
    ls_kd_goal_x_value=arr_kd_goal.tolist()

    # 主队角球时间
    #print('###' * 100)

    arr_zd_corner = np.array(ls_zd_corner_x_value)
    arr_zd_corner = np.round(arr_zd_corner / value_per_min) + 1
    ls_zd_corner_x_value=arr_zd_corner.tolist()

    # 客队角球时间
    #print('###' * 100)
    arr_kd_corner = np.array(ls_kd_corner_x_value)
    arr_kd_corner = np.round(arr_kd_corner / value_per_min) + 1
    ls_kd_corner_x_value=arr_kd_corner.tolist()

    dic = {
           'zd_xy': arr_zd_xy, 'kd_xy': arr_kd_xy,
           'zd_goal': arr_zd_goal, 'kd_goal': arr_kd_goal,
           'zd_corner': arr_zd_corner, 'kd_corner': arr_kd_corner,
           }
    return (dic)


def __fun_table1_shezheng(html_soup,selector):
    dic=_fun_get_orginal_data(html_soup,selector)
    arr_zd_xy_value=dic.get('zd_xy')
    arr_kd_xy_value=dic.get('kd_xy')

    df_zd_cishu = pd.DataFrame(arr_zd_xy_value,columns=['时间','主_射正_数量']).set_index('时间')
    # #print(df_zd_cishu)
    df_kd_cishu = pd.DataFrame(arr_kd_xy_value,columns=['时间','客_射正_数量']).set_index('时间')
    # #print(df_kd_cishu)

    ls_zd_goal=[]
    ls_zd_goal_num=[]
    ls_kd_goal=[]
    ls_kd_goal_num=[]
    for time in dic.get('zd_goal'):
        ls_zd_goal.append(time)
        ls_zd_goal_num.append(len(ls_zd_goal))
    ls_zd_goal_n = list(reversed(ls_zd_goal_num))
    dic_zd_goal={'时间':ls_zd_goal,'主_进球_数量':ls_zd_goal_n}
    df_zd_goal=pd.DataFrame(dic_zd_goal).set_index('时间')
    #print(df_zd_goal)

    for time in dic.get('kd_goal'):
        ls_kd_goal.append(time)
        ls_kd_goal_num.append(len(ls_kd_goal))
    ls_kd_goal_n=list(reversed(ls_kd_goal_num))
    dic_kd_goal={'时间':ls_kd_goal,'客_进球_数量':ls_kd_goal_n}
    df_kd_goal=pd.DataFrame(dic_kd_goal)
    df_kd_goal=df_kd_goal.set_index('时间')
    #print(df_kd_goal)

    ls_zd_corner=[]
    ls_zd_corner_num = []
    ls_kd_corner=[]
    ls_kd_corner_num = []
    for time in dic.get('zd_corner'):
        ls_zd_corner.append(time)
        ls_zd_corner_num.append(len(ls_zd_corner))
    ls_zd_corner_n=list(reversed(ls_zd_corner_num))
    dic_zd_corner = {'时间': ls_zd_corner,'主_角球_数量':ls_zd_corner_n}
    df_zd_corner = pd.DataFrame(dic_zd_corner)
    df_zd_corner=df_zd_corner.set_index('时间')
    #print(df_zd_corner)

    for time in dic.get('kd_corner'):
        ls_kd_corner.append(time)
        ls_kd_corner_num.append(len(ls_kd_corner))
    ls_kd_corner_n=list(reversed(ls_kd_corner_num))
    dic_kd_corner = {'时间': ls_kd_corner,'客_角球_数量':ls_kd_corner_n}
    df_kd_corner = pd.DataFrame(dic_kd_corner)
    df_kd_corner=df_kd_corner.set_index('时间')
    #print(df_kd_corner)
    return (df_zd_cishu,df_kd_cishu,df_zd_goal,df_kd_goal,df_zd_corner,df_kd_corner)
def fun_merge_table1(html_soup,selector):
    df1, df2, df3, df4, df5, df6=__fun_table1_shezheng(html_soup,selector)
    df_tmp1 = pd.merge(df1,df2, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df3,df4, how='outer', left_index=True, right_index=True)
    df_tmp3 = pd.merge(df5, df6, how='outer', left_index=True, right_index=True)
    df_tmp4 = pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    df=pd.merge(df_tmp3, df_tmp4, how='outer', left_index=True, right_index=True)
    #print(df)
    df.to_excel('table1.xlsx')
    return (df)

def __fun_table2_shepian(html_soup,selector):
    dic = _fun_get_orginal_data(html_soup, selector)
    arr_zd_xy_value=dic.get('zd_xy')
    arr_kd_xy_value=dic.get('kd_xy')

    df_zd_cishu = pd.DataFrame(arr_zd_xy_value,columns=['时间','主_射偏_数量']).set_index('时间')
    # #print(df_zd_cishu)
    df_kd_cishu = pd.DataFrame(arr_kd_xy_value,columns=['时间','客_射偏_数量']).set_index('时间')
    # #print(df_kd_cishu)

    ls_zd_goal=[]
    ls_zd_goal_num=[]
    ls_kd_goal=[]
    ls_kd_goal_num=[]
    for time in dic.get('zd_goal'):
        ls_zd_goal.append(time)
        ls_zd_goal_num.append(len(ls_zd_goal))
    ls_zd_goal_n = list(reversed(ls_zd_goal_num))
    dic_zd_goal={'时间':ls_zd_goal,'主_进球_数量':ls_zd_goal_n}
    df_zd_goal=pd.DataFrame(dic_zd_goal).set_index('时间')
    #print(df_zd_goal)

    for time in dic.get('kd_goal'):
        ls_kd_goal.append(time)
        ls_kd_goal_num.append(len(ls_kd_goal))
    ls_kd_goal_n=list(reversed(ls_kd_goal_num))
    dic_kd_goal={'时间':ls_kd_goal,'客_进球_数量':ls_kd_goal_n}
    df_kd_goal=pd.DataFrame(dic_kd_goal)
    df_kd_goal=df_kd_goal.set_index('时间')
    #print(df_kd_goal)

    ls_zd_corner=[]
    ls_zd_corner_num = []
    ls_kd_corner=[]
    ls_kd_corner_num = []
    for time in dic.get('zd_corner'):
        ls_zd_corner.append(time)
        ls_zd_corner_num.append(len(ls_zd_corner))
    ls_zd_corner_n=list(reversed(ls_zd_corner_num))
    dic_zd_corner = {'时间': ls_zd_corner,'主_角球_数量':ls_zd_corner_n}
    df_zd_corner = pd.DataFrame(dic_zd_corner)
    df_zd_corner=df_zd_corner.set_index('时间')
    #print(df_zd_corner)

    for time in dic.get('kd_corner'):
        ls_kd_corner.append(time)
        ls_kd_corner_num.append(len(ls_kd_corner))
    ls_kd_corner_n=list(reversed(ls_kd_corner_num))
    dic_kd_corner = {'时间': ls_kd_corner,'客_角球_数量':ls_kd_corner_n}
    df_kd_corner = pd.DataFrame(dic_kd_corner)
    df_kd_corner=df_kd_corner.set_index('时间')
    #print(df_kd_corner)
    return (df_zd_cishu,df_kd_cishu,df_zd_goal,df_kd_goal,df_zd_corner,df_kd_corner)
def fun_merge_table2(html_soup,selector):
    df1, df2, df3, df4, df5, df6=__fun_table2_shepian(html_soup,selector)
    df_tmp1 = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df3, df4, how='outer', left_index=True, right_index=True)
    df_tmp3 = pd.merge(df5, df6, how='outer', left_index=True, right_index=True)
    df_tmp4 = pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    df = pd.merge(df_tmp3, df_tmp4, how='outer', left_index=True, right_index=True)
    #print(df)
    df.to_excel('table2.xlsx')
    return (df)

def __fun_table3_weixian(html_soup,selector):
    dic = _fun_get_orginal_data(html_soup, selector)
    arr_zd_xy_value=dic.get('zd_xy')
    arr_kd_xy_value=dic.get('kd_xy')

    df_zd_cishu = pd.DataFrame(arr_zd_xy_value,columns=['时间','主_危险进攻_数量']).set_index('时间')
    # #print(df_zd_cishu)
    df_kd_cishu = pd.DataFrame(arr_kd_xy_value,columns=['时间','客_危险进攻_数量']).set_index('时间')
    # #print(df_kd_cishu)

    ls_zd_goal=[]
    ls_zd_goal_num=[]
    ls_kd_goal=[]
    ls_kd_goal_num=[]
    for time in dic.get('zd_goal'):
        ls_zd_goal.append(time)
        ls_zd_goal_num.append(len(ls_zd_goal))
    ls_zd_goal_n = list(reversed(ls_zd_goal_num))
    dic_zd_goal={'时间':ls_zd_goal,'主_进球_数量':ls_zd_goal_n}
    df_zd_goal=pd.DataFrame(dic_zd_goal).set_index('时间')
    #print(df_zd_goal)

    for time in dic.get('kd_goal'):
        ls_kd_goal.append(time)
        ls_kd_goal_num.append(len(ls_kd_goal))
    ls_kd_goal_n=list(reversed(ls_kd_goal_num))
    dic_kd_goal={'时间':ls_kd_goal,'客_进球_数量':ls_kd_goal_n}
    df_kd_goal=pd.DataFrame(dic_kd_goal)
    df_kd_goal=df_kd_goal.set_index('时间')
    #print(df_kd_goal)

    ls_zd_corner=[]
    ls_zd_corner_num = []
    ls_kd_corner=[]
    ls_kd_corner_num = []
    for time in dic.get('zd_corner'):
        ls_zd_corner.append(time)
        ls_zd_corner_num.append(len(ls_zd_corner))
    ls_zd_corner_n=list(reversed(ls_zd_corner_num))
    dic_zd_corner = {'时间': ls_zd_corner,'主_角球_数量':ls_zd_corner_n}
    df_zd_corner = pd.DataFrame(dic_zd_corner)
    df_zd_corner=df_zd_corner.set_index('时间')
    #print(df_zd_corner)

    for time in dic.get('kd_corner'):
        ls_kd_corner.append(time)
        ls_kd_corner_num.append(len(ls_kd_corner))
    ls_kd_corner_n=list(reversed(ls_kd_corner_num))
    dic_kd_corner = {'时间': ls_kd_corner,'客_角球_数量':ls_kd_corner_n}
    df_kd_corner = pd.DataFrame(dic_kd_corner)
    df_kd_corner=df_kd_corner.set_index('时间')
    #print(df_kd_corner)
    return (df_zd_cishu,df_kd_cishu,df_zd_goal,df_kd_goal,df_zd_corner,df_kd_corner)
def fun_merge_table3(html_soup,selector):
    df1, df2, df3, df4, df5, df6 = __fun_table3_weixian(html_soup, selector)
    df_tmp1 = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df3, df4, how='outer', left_index=True, right_index=True)
    df_tmp3 = pd.merge(df5, df6, how='outer', left_index=True, right_index=True)
    df_tmp4 = pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    df = pd.merge(df_tmp3, df_tmp4, how='outer', left_index=True, right_index=True)
    #print(df)
    df.to_excel('table3.xlsx')
    return (df)

def __fun_table4_jingong(html_soup,selector):
    dic = _fun_get_orginal_data(html_soup, selector)
    arr_zd_xy_value=dic.get('zd_xy')
    arr_kd_xy_value=dic.get('kd_xy')

    df_zd_cishu = pd.DataFrame(arr_zd_xy_value,columns=['时间','主_进攻_数量']).set_index('时间')
    # #print(df_zd_cishu)
    df_kd_cishu = pd.DataFrame(arr_kd_xy_value,columns=['时间','客_进攻_数量']).set_index('时间')
    # #print(df_kd_cishu)

    ls_zd_goal=[]
    ls_zd_goal_num=[]
    ls_kd_goal=[]
    ls_kd_goal_num=[]
    for time in dic.get('zd_goal'):
        ls_zd_goal.append(time)
        ls_zd_goal_num.append(len(ls_zd_goal))
    ls_zd_goal_n = list(reversed(ls_zd_goal_num))
    dic_zd_goal={'时间':ls_zd_goal,'主_进球_数量':ls_zd_goal_n}
    df_zd_goal=pd.DataFrame(dic_zd_goal).set_index('时间')
    #print(df_zd_goal)

    for time in dic.get('kd_goal'):
        ls_kd_goal.append(time)
        ls_kd_goal_num.append(len(ls_kd_goal))
    ls_kd_goal_n=list(reversed(ls_kd_goal_num))
    dic_kd_goal={'时间':ls_kd_goal,'客_进球_数量':ls_kd_goal_n}
    df_kd_goal=pd.DataFrame(dic_kd_goal)
    df_kd_goal=df_kd_goal.set_index('时间')
    #print(df_kd_goal)

    ls_zd_corner=[]
    ls_zd_corner_num = []
    ls_kd_corner=[]
    ls_kd_corner_num = []
    for time in dic.get('zd_corner'):
        ls_zd_corner.append(time)
        ls_zd_corner_num.append(len(ls_zd_corner))
    ls_zd_corner_n=list(reversed(ls_zd_corner_num))
    dic_zd_corner = {'时间': ls_zd_corner,'主_角球_数量':ls_zd_corner_n}
    df_zd_corner = pd.DataFrame(dic_zd_corner)
    df_zd_corner=df_zd_corner.set_index('时间')
    #print(df_zd_corner)

    for time in dic.get('kd_corner'):
        ls_kd_corner.append(time)
        ls_kd_corner_num.append(len(ls_kd_corner))
    ls_kd_corner_n=list(reversed(ls_kd_corner_num))
    dic_kd_corner = {'时间': ls_kd_corner,'客_角球_数量':ls_kd_corner_n}
    df_kd_corner = pd.DataFrame(dic_kd_corner)
    df_kd_corner=df_kd_corner.set_index('时间')
    #print(df_kd_corner)
    return (df_zd_cishu,df_kd_cishu,df_zd_goal,df_kd_goal,df_zd_corner,df_kd_corner)
def fun_merge_table4(html_soup,selector):
    df1, df2, df3, df4, df5, df6=__fun_table4_jingong(html_soup,selector)
    df_tmp1 = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df3, df4, how='outer', left_index=True, right_index=True)
    df_tmp3 = pd.merge(df5, df6, how='outer', left_index=True, right_index=True)
    df_tmp4 = pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    df = pd.merge(df_tmp3, df_tmp4, how='outer', left_index=True, right_index=True)
    #print(df)
    df.to_excel('table4.xlsx')
    return (df)

def fun_get_xc_gongfang(html_soup):
    #table1
    selector='#highcharts-0 > svg > g '     #四张图依次是0 4 8 12
    df_talbe1=fun_merge_table1(html_soup,selector)
    # print(list(df_talbe1.columns))
    df1=df_talbe1[['主_角球_数量', '客_角球_数量', '主_射正_数量', '客_射正_数量', '主_进球_数量', '客_进球_数量']]

    #table2
    selector='#highcharts-4 > svg > g '     #四张图依次是0 4 8 12
    df_talbe2=fun_merge_table2(html_soup,selector)
    df2=df_talbe2[['主_射偏_数量','客_射偏_数量']]
    #table3
    selector='#highcharts-8 > svg > g '     #四张图依次是0 4 8 12
    df_talbe3=fun_merge_table3(html_soup,selector)
    df3=df_talbe3[['主_危险进攻_数量','客_危险进攻_数量']]
    #table4
    selector='#highcharts-12 > svg > g '     #四张图依次是0 4 8 12
    df_talbe4=fun_merge_table4(html_soup,selector)
    df4=df_talbe4[['主_进攻_数量','客_进攻_数量']]
    return (df1,df2,df3,df4)

def fun_main_adjust_gongfang_table(html_soup):
    df1,df2,df3,df4=fun_get_xc_gongfang(html_soup)
    df_tmp1 = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    df_tmp2 = pd.merge(df3, df4, how='outer', left_index=True, right_index=True)
    df= pd.merge(df_tmp1, df_tmp2, how='outer', left_index=True, right_index=True)
    # print(df)

    # #对合并后的总表进行处理

    df=df.sort_values(by=['主_进攻_数量','客_进攻_数量','主_危险进攻_数量','客_危险进攻_数量'])
    df=df.sort_index()
    df = df.loc[~df.index.duplicated(keep='last')]  # 时间去重，只保留第一个
    # df.to_excel('table_all_01.xlsx')
    return (df)

if __name__=='__main__':
    df = pd.DataFrame()
    with open('temp.html', 'rb') as f1:
        html = f1.read()
    html_soup = BeautifulSoup(html, 'lxml')

    fun_main_adjust_gongfang_table(html_soup)




