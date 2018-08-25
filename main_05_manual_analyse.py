import pandas as pd
import os

def fun_goal(df_orgianl):
    df=df_orgianl.copy()
    df['结果偏差']=df['预测结果']-df['真实结果']
    try:
        goal=list(df['预测结果'])[0]
    except:
        goal=100    #代表为空，没有符合要求的比赛
    print('#'*10)
    ##################################################################
    jifa_max=df['激发量'].max()
    jifa_min=df['激发量'].min()
    print('本次结果中最大的激活量是：{}'.format(jifa_max))
    print('本次结果中最小的激活量是：{}'.format(df['激发量'].min()))
    ##################################################################
    ls_rate=[]  #生成的密度
    for i in range(100):
        ls_rate.append(i/100)

    ls_yuce_result=[]
    ls_jihuoliang=[]
    ls_defen=[]
    ls_num_cal=[]
    ls_num_true=[]
    ls_jifa_value=[]

    print(list(df.columns))
    ###########################################################
    for rate in ls_rate:
        num_big = (jifa_max - jifa_min) * rate + jifa_min
        ls_jifa_value.append(round(num_big,2))
        if goal==0:
            df1=df[df['激发量']>num_big]
            df_cal_0=df1[df1['预测结果']==0]
            df_true_0=df_cal_0[df_cal_0['真实结果']==0]
            num_cal=df_cal_0['预测结果'].count()
            num_true=df_true_0['真实结果'].count()
            if num_cal != 0:
                score = num_true / num_cal
                score = round(score, 3)
            else:
                score = 0

            ls_yuce_result.append(goal)
            ls_jihuoliang.append(rate)
            ls_defen.append(score)
            ls_num_cal.append(num_cal)
            ls_num_true.append(num_true)

            print('A预测结果：{},B激活量百分比：{},#####C得分：{} ######,D比赛数量：{},E正确数量{}'.format(goal,rate,score,num_cal,num_true))

        elif goal==100:
            # 代表为空，没有符合要求的比赛
            ls_yuce_result.append(100)
            ls_jihuoliang.append(100)
            ls_defen.append(100)
            ls_num_cal.append(100)
            ls_num_true.append(100)
            pass

        else:
            df1=df[df['激发量']>num_big]
            df_cal_0=df1[df1['预测结果']==goal]
            df_true_0=df_cal_0[df_cal_0['真实结果']>=goal]
            num_cal=df_cal_0['预测结果'].count()
            num_true=df_true_0['真实结果'].count()
            if num_cal !=0:
                score=num_true/num_cal
                score = round(score, 3)
            else:
                score=0

            ls_yuce_result.append(goal)
            ls_jihuoliang.append(rate)
            ls_defen.append(score)
            ls_num_cal.append(num_cal)
            ls_num_true.append(num_true)
            print('A预测结果：{},B激活量百分比：{},C得分：{},D比赛数量：{},E正确数量{}'.format(goal, rate, score, num_cal, num_true))

    dic={'预测结果':ls_yuce_result,'激活量百分比':ls_jihuoliang,'得分':ls_defen,'预测比赛数量':ls_num_cal,'正确数量':ls_num_true,
         '激发量_值':ls_jifa_value
         }

    df_end=pd.DataFrame(dic)
    ls=['预测结果','得分','预测比赛数量', '正确数量','激活量百分比', '激发量_值' ]
    df_end=df_end.reindex(columns=ls)
    return(df_end)

from fun_make_table import make_sp_xc_table

def fun_score_valid(x):
    if x >=30:
        x=1
    else:
        x=0
    return (x)

def main_analyse(ls_models):
    for model_name in ls_models:
        print('*'*40)
        print('当前分析模型为 {}'.format(model_name))
        path_result='ds_data_test\\'+model_name+'\\'+'test_result'
        ls=os.listdir(path_result)
        xlsx=''
        for name in ls:
            if 'test' in name:
                xlsx=name
            else:
                print('在模型中没有测试数据')
        path_read=path_result+'\\'+xlsx
        df=pd.read_excel(path_read)
        ls_goal=[0,1,2,3]
        print(list(df.columns))
        for goal in ls_goal:
            print('#'*10)
            print('预测结果为有{}球'.format(goal))
            df_goal=df[df['预测结果']==goal]
            df_end=fun_goal(df_goal)
            ##############################################
            #对df_end进行插值，形成一个可以查询的表格
            df_final=make_sp_xc_table.make_score_table(df_end)
            #预测的比赛 数量大于30 场以上的才是有效预测
            df_final['得分有效位']=df_final['预测比赛数量'].apply(fun_score_valid)

            path_save='ds_data_test\\'+model_name+'\\'+'goal_check_'+str(goal)+'.xlsx'
            df_final.to_excel(path_save)

def main_analyse_for_now(model_name):
    path= 'ds_data_test\\'+model_name
    path_file = path + '\\test_result\\now.xlsx'

    df = pd.read_excel(path_file)
    df['激发量'] = df['激发量'].apply(lambda x: round(x, 2))
    print("###01###")
    print(df)
    print(list(df.columns))
    df_hebing = pd.DataFrame()  #最终返回值
    ls_goal = [0, 1, 2, 3]
    for goal in ls_goal:
        df_goal = df[df['预测结果'] == goal]

        path_goal = path + '\\goal_check_' + str(goal) + '.xlsx'
        df_score = pd.read_excel(path_goal)

        df_end = pd.merge(df_goal, df_score, left_on='激发量', right_on='激发量_值', how='inner')
        ls = ['联赛名称', '主队名称', '客名_跨值', '预测结果_x',
              '激发量', '真实结果', '本场比赛ID', 'index', '预测结果_y', '得分',
              '预测比赛数量', '正确数量', '激活量百分比', '激发量_值', '得分有效位']
        ls_final = ['本场比赛ID', '联赛名称', '主队名称', '客名_跨值', '预测结果_x', '得分']

        df_final = df_end[df_end['得分有效位'] == 1]
        df_final = df_final.reindex(columns=ls_final)
        print(df_final)
        print('#' * 20)
        if not df_final.empty:
            df_hebing=df_hebing.append(df_final)
    print("###02###")
    print(df_hebing)
    return (df_hebing)
    pass

def fun_analyse_manual(ls_models):
    for model_name in ls_models:
        print('*'*40)
        print('当前手动分析模型为 {}'.format(model_name))
        path_result='ds_data_test\\'+model_name+'\\'+'test_result'
        ls=os.listdir(path_result)
        xlsx=''
        for name in ls:
            if 'test' in name:
                xlsx=name
            else:
                print('在模型中没有测试数据')
        path_read = path_result + '\\' + xlsx
        df = pd.read_excel(path_read)
        #######################################################
        ls_goal=[0,1,2,3]
        print(list(df.columns))
        for goal in ls_goal:
            df_goal=df[df['预测结果']==goal]
            df_goal_2=df_goal[df_goal['预测结果调整']>=0]
            df_goal_2_real=df_goal_2[df_goal_2['真实结果']>=(goal+1)]
            df_test=df_goal_2[df_goal_2['真实结果']>=goal]
            total=df_goal_2['预测结果调整'].count()
            ying=df_goal_2_real['真实结果'].count()
            ping=df_test['真实结果'].count()
            score_ying=ying/total
            score_ping=round(ping/total-score_ying,2)
            score_shu=round(1-score_ying-score_ping,2)

            print('比分为{},::::赢的机会{},平的机会{},输的机会{}'.format(goal,score_ying,score_ping,score_shu))


    pass

if __name__=='__main__':

    ######################################################
    # model_name='model_2'
    # main_analyse_for_now(model_name)
    ######################################################
    # ls_models = [ 'model_2', 'model_2_0','model_2_0_1','model_2_0_2','model_2_0_3', 'model_2_0_4',
    #                     'model_2_1','model_2_1_2','model_2_1_3','model_2_1_4',
    #                     'model_2_2', 'model_2_3', 'model_2_4']
    # ls_models =['model_2_1_4']
    # ls_models = ['model_1', 'model_1_0', 'model_1_0_1', 'model_1_0_2', 'model_1_0_3', 'model_1_1', 'model_1_2',
    #                'model_1_3', 'model_1_4']
    # ls_models = ['model_2_sp','model_2_sp_1','model_2_sp_1_2','model_2_sp_2']
#######################################
    # ls_models = ['model_1', 'model_1_0', 'model_1_0_1', 'model_1_0_2', 'model_1_0_3', 'model_1_1', 'model_1_2',
    #              'model_1_3', 'model_1_4',
    #              'model_2', 'model_2_0', 'model_2_0_1', 'model_2_0_2', 'model_2_0_3', 'model_2_0_4', 'model_2_1',
    #              'model_2_1_2', 'model_2_1_3',
    #              'model_2_1_4', 'model_2_2', 'model_2_3', 'model_2_4',
    #              'model_2_sp', 'model_2_sp_0_2', 'model_2_sp_1', 'model_2_sp_1', 'model_2_sp_1.5_5', 'model_2_sp_1_2',
    #              'model_2_sp_2'
    #              ]
    ls_models = ['model_2_sp']

    # main_analyse(ls_models)
    fun_analyse_manual(ls_models)
##########################################









