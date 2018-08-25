#!/usr/bin/env python
# -*- coding:utf-8 -*-
###第一章节
#############################################
# from sklearn import datasets
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
#
# ##############################
# #数据库操作
# iris = datasets.load_iris()
# iris_X = iris.data
# iris_y = iris.target
# #############################
# #生成训练数据和测试数据
# X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3) #0.3 测试数据占比30%
# #############################
# #生成模型
# knn = KNeighborsClassifier()
# #训练模型
# knn.fit(X_train, y_train)   #监督学习
# #############################
# #使用测试组进行检验
# print(knn.predict(X_test))
# print(y_test)

####################

# from sklearn import datasets
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
#
# loaded_data = datasets.load_boston()
# data_X = loaded_data.data
# data_y = loaded_data.target
#
# model = LinearRegression()
# model.fit(data_X, data_y)
#
# ax1=model.predict(data_X[:4, :])
# ax2=data_y[:4]
# print(model.get_params())
# xx=model.score(data_X,data_y)
# print(xx)


from sklearn import preprocessing #标准化数据模块
import numpy as np
#建立Array
a = np.array([[10, 2.7, 3.6],
              [-100, 5, -2],
              [120, 20, 40]], dtype=np.float64)
#将normalized后的a打印出
print(preprocessing.scale(a))
