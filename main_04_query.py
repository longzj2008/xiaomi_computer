#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy
import os
import scipy.special
import pandas as pd
import matplotlib.pyplot
class nenralNetwork:
    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate,wih,who):
        self.inodes=inputnodes
        self.hnodes=hiddennodes
        self.onodes=outputnodes

        self.wih=wih
        self.who=who

        self.lr=learningrate

        self.activation_function=lambda x: scipy.special.expit(x)
        #expit(x) = 1/(1+exp(-x)).
        pass

    def query(self,inputs_list):
        #变换列表到二维数组
        inputs=numpy.array(inputs_list,ndmin=2).T

        # 计算输入信号到隐藏层
        hidden_inputs = numpy.dot(self.wih, inputs)
        # 计算隐藏层的激发信号
        hidden_outputs = self.activation_function(hidden_inputs)
        # 计算隐藏层信号到输出层
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # 计算输出层的输出
        final_outputs = self.activation_function(final_inputs)
        return (final_outputs)

def fun_adjust_yuce(ls,label,step=0.25):

    yuce=label+0.5
    #################
    #查询周围值的情况
    v=ls[label]
    try:
        v_be=ls[label-1]
    except:
        v_be=0
    try:
        v_af=ls[label+1]
    except:
        v_af=0
    #####################
    #门槛值设定
    th_1=v*step*1       #0.25
    th_2=v*step*2       #0.5
    th_3=v*step*3       #0.75

    #######################
    #根据前一个值情况调整
    if v_be !=0:
        if v_be>th_3:
            yuce=yuce-0.25
        elif v_be>th_2 and v_be<th_3:
            yuce=yuce-0.12
        elif v_be>th_1 and v_be<th_2:
            yuce=yuce-0.06

    #######################
    #根据后一个值情况调整
    if v_af !=0:
        if v_af>th_3:
            yuce=yuce+0.25
        elif v_af>th_2 and v_af<th_3:
            yuce=yuce+0.12
        elif v_af>th_1 and v_af<th_2:
            yuce=yuce+0.06

    return (yuce)

def main_query_model(file_name,model_name,lenth):
    ###################################################################################
    # 设定参数
    input_nodes = lenth
    hidden_nodes = lenth
    output_nodes = 4
    learning_rate = 0.01
    ###################################################################################
    # 共用路径的设置

    path_weigh_who = 'ds_model_weigh' + '\\' + model_name + '\\' + 'who.txt'
    path_weigh_wih = 'ds_model_weigh' + '\\' + model_name + '\\' + 'wih.txt'
    # 专用路径的设置
    path_tests = 'ds_data_train' + '\\' + model_name
    path_result_save = 'ds_data_test' + '\\' + model_name + '\\' + 'test_result' + '\\'
    ###################################################################################
    # 读取相应模型的权重
    wih = numpy.loadtxt(path_weigh_wih)
    who = numpy.loadtxt(path_weigh_who)
    ###################################################################################
    # 创建一个神经网络
    n = nenralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate, wih, who)
    ###################################################################################
    # 开始测试
    # 读取训练用数据库
    ls_xlsxs = os.listdir(path_tests)
    ####################################################
    #通过下面的判断，默认对data_all 中的所有表进行生产模型，如果输入文件名，那么只对数据的名字进行处理
    ls_xlsxs_final=[]
    if file_name=='':
        ls_xlsxs_final=ls_xlsxs
    else:
        for name in ls_xlsxs:
            if file_name in name:
                ls_xlsxs_final.append(name)

    for xlsx in ls_xlsxs_final:
        # 测试神经网络
        # 定义一些存储列表，下次情况
        ls_cal_result = []  # 计算结论
        ls_cal_result_adjust=[]#根据前后激活量，对预测值进行调整
        ls_target_range=[]  #目标范围
        ls_true_result = []  # 真实结果
        ls_active_value = []  # 激活量的值
        ls_id = []  # 比赛ID
        ls_league_name = []  # 联赛名称
        ls_zd_name = []  # 主队名称
        ls_kd_name = []  # 客队名称

        if '.xlsx' in xlsx:  # 排除文件夹干扰
            path_xlsx = path_tests + '\\' + xlsx
            print(path_xlsx)
            df_test = pd.read_excel(path_xlsx)
            test_data_list = df_test.values
            # 开始测试
            print('测试数据的数量为：{}'.format(len(test_data_list)))
            print('开始计算测试数据，请稍等')
            num = 1
            for record in test_data_list:
                # print('#{}'.format(num),end='')
                num += 1
                # 提取目标
                # correct_label = int(record[6])
                # 对输入进行缩小和平移
                inputs = (numpy.asfarray(record[7:]) + 5) / 20  # 范围为-5~15
                # 使用类函数获得输出
                outputs = n.query(inputs)
                # 最大值的索引就是标签,下面这个函数返回最大值的索引
                label = numpy.argmax(outputs)
                # 对所有量进行记录,存储，方便手动分析
                #['本场比赛ID', '联赛名称', '主_名字', '半sp跨值','初盘_让球','全球和','目标', '初盘_大小','半球和']
                ls_cal_result.append(label) #预测结果
                #######################################
                #根据前后激活值的大小，调整预测值
                ls=list(outputs.T[0])
                yuce_adjust=fun_adjust_yuce(ls,label)
                ls_cal_result_adjust.append(yuce_adjust)
                ls_active_value.append(outputs[label][0])   #之所以[0]，是因为output[label]是个1个数据的列表
                ###################################
                ls_id.append(record[0])
                ls_league_name.append(record[1])
                ls_zd_name.append(record[2])
                ls_kd_name.append(record[3])
                ls_true_result.append(round(record[5]-record[8]))  #全球和-半球和

            dic = {'本场比赛ID': ls_id, '联赛名称': ls_league_name, '主队名称': ls_zd_name, '客名_跨值': ls_kd_name,
                   '预测结果': ls_cal_result,'预测结果调整':ls_cal_result_adjust, '真实结果': ls_true_result, '激发量': ls_active_value, }
            df_tmp = pd.DataFrame(dic,columns=['联赛名称','主队名称','客名_跨值','预测结果','预测结果调整','激发量','真实结果','本场比赛ID'])
            df_tmp.to_excel(path_result_save + xlsx)
            print("计算结果已经存储在:{}".format(path_result_save + xlsx))

    print('处理完毕')
    return(df_tmp)


if __name__=='__main__':

    file_name='test'    #其实是文件名中包括
    ls_models = [ 'model_2_sp']
    for model_name in ls_models:
        print('#'*30)
        print('测试模型 {},测试文件为：{}'.format(model_name,file_name))
        if 'model_2' in model_name:
            lenth = 409 - 7
        elif 'model_1' in model_name:
            lenth = 236 - 5
        else:
            print('错:{}'.format(model_name))
            lenth=0
            break
        main_query_model(file_name,model_name,lenth)


