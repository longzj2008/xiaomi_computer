#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy
import scipy.special
import pandas as pd
import matplotlib.pyplot
import os
class nenralNetwork:
    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
        self.inodes=inputnodes
        self.hnodes=hiddennodes
        self.onodes=outputnodes

        self.wih=numpy.random.normal(0.0,pow(self.hnodes,-0.5),(self.hnodes,self.inodes))
        self.who=numpy.random.normal(0.0,pow(self.onodes,-0.5),(self.onodes,self.hnodes))

        self.lr=learningrate

        self.activation_function=lambda x: scipy.special.expit(x)
        #expit(x) = 1/(1+exp(-x)).
        pass
    #train the network
    def train(self,inputs_list,targets_list):
        #输入信号
        inputs=numpy.array(inputs_list,ndmin=2).T
        #目标信号
        targets=numpy.array(targets_list,ndmin=2).T

        #计算输入信号到隐藏层
        hidden_inputs=numpy.dot(self.wih,inputs)
        #计算隐藏层的激发信号
        hidden_outputs=self.activation_function(hidden_inputs)
        #计算隐藏层信号到输出层
        final_inputs=numpy.dot(self.who,hidden_outputs)
        #计算输出层的输出
        final_outputs=self.activation_function(final_inputs)

        #计算偏差
        output_errors=targets-final_outputs
        #向前传导，推出 隐藏层的错误偏差
        hidden_errors=numpy.dot(self.who.T,output_errors)
        #升级隐藏层与输出层的权重
        self.who+=self.lr*numpy.dot((output_errors*final_outputs*(1.0-final_outputs)),numpy.transpose(hidden_outputs))
        #升级输入层与隐藏层的权重
        self.wih+=self.lr*numpy.dot((hidden_errors*hidden_outputs*(1.0-hidden_outputs)),numpy.transpose(inputs))
        return (self.who,self.wih)

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

def main_train(model_name,lenth):
    # 设定参数
    input_nodes = lenth
    hidden_nodes = lenth
    output_nodes = 4
    learning_rate = 0.01

    ls_cal_result = []
    ls_true_result = []
    ls_active = []
    ls_id = []
    ls_active_all = []

    #########################################
    # 共用路径的设置
    path_weigh_who = 'ds_model_weigh' + '\\' + model_name + '\\' + 'who.txt'
    path_weigh_wih = 'ds_model_weigh' + '\\' + model_name + '\\' + 'wih.txt'
    # 专用路径设置
    path_trains = 'ds_data_train' + '\\' + model_name
    ##################################################
    # 创建一个神经网络
    n = nenralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    ###################################################
    # 训练神经网络
    # 读取训练用数据库
    ls_xlsxs_final = []
    ls_xlsxs = os.listdir(path_trains)
    #########################################################
    # 这里做一下排除
    for xlsx in ls_xlsxs:
        if 'now' in xlsx:
            pass
        elif 'test' in xlsx:
            pass
        else:
            ls_xlsxs_final.append(xlsx)
            #########################################################
    # 开始训练
    num = 0
    for xlsx in ls_xlsxs_final:
        path_xlsx = path_trains + '\\' + xlsx
        df_trian = pd.read_excel(path_xlsx)
        #########################################################
        training_data_list = df_trian.values
        num = num + 1
        print('数据表共：{},当前为第：{},名称为:{}'.format(len(ls_xlsxs), num, xlsx))
        print('当前数据表：比赛的数量为：{}'.format(len(training_data_list)))
        print('开始训练，请稍等')
        # 开始训练
        # 定义一个世代，这组数据被训练的次数
        epochs = 5
        for e in range(epochs):
            print('当前训练的世代为{}'.format(e))
            for record in training_data_list:
                # 对输入进行缩小和平移
                inputs = (numpy.asfarray(record[7:]) + 5) / 20  # 范围为-5~15
                # 创建目标结果列表，所有都设为0.01，除了要求的是0.99
                targets = numpy.zeros(output_nodes) + 0.001
                #######################################
                #当 targets 为两个时
                # if int(record[4]) == 0:
                #     targets[int(record[4])] = 0.99  # 没球的给0.80的激活量
                # else:
                #     targets[int(record[4])] = 0.99  # 有球的给0.99的激活量，鼓励判断有球
                #######################################
                #当 targets为多个时

                targets[int(record[6])]=0.99    #对应进球个数

                # 开始训练

                who, wih = n.train(inputs, targets)
                pass
                ######################################
    # 对训练结果进行存储
    numpy.savetxt(path_weigh_who, who)
    numpy.savetxt(path_weigh_wih, wih)
    print("训练完毕！！")

if __name__=='__main__':
     # ls_models=['model_1','model_1_0','model_1_0_1','model_1_0_2','model_1_0_3','model_1_1','model_1_2','model_1_3','model_1_4']
    # 'model_2', 'model_2_0','model_2_0_1','model_2_0_2','model_2_0_3',
    #'model_2_0_4','model_2_1','model_2_1_2','model_2_1_3','model_2_1_4'
    #'model_2_2', 'model_2_3', 'model_2_4'
     # ls_models_2 = [
     #                'model_2_0_4','model_2_1_4'
     #                ]
    # ls_models=['model_2_sp','model_2_sp_1','model_2_sp_1_2','model_2_sp_2']
    ls_models = ['model_2_sp','model_2_sp_t_1']
    lenth=0
    for model_name in ls_models:
     print('#'*30)
     print('测试模型 {}'.format(model_name))
     if 'model_2' in model_name:
         lenth = 409 - 7
     elif 'model_1' in model_name:
         lenth = 236 - 5

     main_train(model_name,lenth)







