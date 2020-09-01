# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2020/8/4 14:03
# IDE：PyCharm
# https://www.cnblogs.com/liu247/p/11152875.html
# https://blog.csdn.net/out_of_memory_error/article/details/81414986

import torch
import torch.nn.functional as F
from torch import nn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc, accuracy_score


# 包含了一个输入层、一个隐层、一个输出层的神经网络。
class Net(nn.Module):
    def __init__(self,n_feature,n_hidden_1, n_hidden_2,n_output):
        """
        :param n_feature:
        :param n_hidden_1:
        :param n_hidden_2:
        :param n_output: 数据类别的数目，二分类问题该变量值就是2
        """
        super(Net,self).__init__()
        self.hidden_1 = nn.Linear(n_feature, n_hidden_1)
        self.hidden_2 = nn.Linear(n_hidden_1, n_hidden_2)
        self.output  = nn.Linear(n_hidden_2, n_output)

    def forward(self, x):
        x = self.hidden_1(x)
        x = torch.sigmoid(x)
        x = self.hidden_2(x)
        x = torch.sigmoid(x)
        x = self.output(x)
        return x

if __name__ == '__main__':
    train_data = pd.read_excel("data_train.xlsx", header=0)
    test_data = pd.read_excel("data_test.xlsx", header=0)

    # 划分训练集、验证集，加工测试集
    X, y = train_data.drop(columns=["phone_no_m", "label"]), train_data["label"].values
    test_X= test_data.drop(columns=["phone_no_m", "label"])
    nb_samples, nb_features = np.shape(X)
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)
    train_X, train_y = torch.from_numpy(train_X.values).float(), torch.from_numpy(train_y).long()
    test_X = torch.from_numpy(test_X.values).float()

    find_level = pd.DataFrame(columns=["first_level", "second_level", "roc_auc_score"])
    for first_level in (10, 20, 30, 40):
        for second_level in (10, 20, 30, 40):
            print(str(first_level)+"--->"+str(second_level))
            net = Net(nb_features, first_level, second_level, 2)
            optimizer = torch.optim.SGD(net.parameters(), lr=0.1)
            loss_func = torch.nn.CrossEntropyLoss()

            for i in range(5000):
                prediction = net(train_X)
                loss = loss_func(prediction, train_y)

                # 梯度归零
                optimizer.zero_grad()
                # 计算梯度
                loss.backward()
                # 更新结点
                optimizer.step()
            x1 = torch.FloatTensor(val_X.values)
            val_y_predict = F.softmax(net(x1), 1)
            val_y_predict_prob = [round(float(x[1]), 3) for x in val_y_predict]
            find_level = find_level.append(pd.DataFrame(
                {"first_level": [first_level],
                 "second_level": [second_level],
                 "roc_auc_score": [roc_auc_score(val_y, val_y_predict_prob)]}
            ))


    net = Net(nb_features, 20, 30, 2)
    optimizer = torch.optim.SGD(net.parameters(), lr=0.1)
    loss_func = torch.nn.CrossEntropyLoss()

    # 训练神经网络
    for i in range(5000):
        prediction = net(train_X)
        loss = loss_func(prediction, train_y)

        # 梯度归零
        optimizer.zero_grad()
        # 计算梯度
        loss.backward()
        # 更新结点
        optimizer.step()
        if i % 100 == 0:
            print("--- "+str(i))
            print(loss)

    x1 = torch.FloatTensor(val_X.values)
    val_y_predict = F.softmax(net(x1), 1)
    val_y_predict_prob = [round(float(x[1]), 3) for x in val_y_predict]
    roc_auc_score(val_y, val_y_predict_prob)

    fpr, tpr, thresholds = roc_curve(val_y, val_y_predict_prob)
    print(auc(fpr, tpr))

    # 计算各阈值对应的约登指数
    you_den = [tpr[i]-fpr[i] for i in range(len(fpr))]
    # 取约登指数最大的阈值为临界点
    threshold = thresholds[you_den.index(max(you_den))]

    # 计算约登指数最大的阈值为临界点的准确率
    val_y_predict = [0 if x<threshold else 1 for x in val_y_predict_prob]
    accuracy_score(val_y, val_y_predict)

    # 根据准确率计算准确率最高时的阈值
    threshold_result = pd.DataFrame(columns=["threshold", "accuracy"])
    for current_threshold in thresholds:
        val_y_predict = [0 if x < current_threshold else 1 for x in val_x_predict_prob]
        threshold_result = threshold_result.append(
            pd.DataFrame({
                "threshold": [current_threshold],
                "accuracy": [accuracy_score(val_y, val_y_predict)]
            })
        )
    threshold_result.reset_index(drop=True, inplace=True)
    best_accuracy_threshold = threshold_result["threshold"].values[
        threshold_result["accuracy"].values.tolist().index(max(threshold_result["accuracy"].values))]

    # 测试数据
    test_y_prob = torch.softmax(net(test_X), 1)
    test_y = [1 if x[1]>=threshold else 0 for x in test_y_prob]

    final_result = pd.DataFrame({
        "phone_no_m": test_data["phone_no_m"].values,
        "label": test_y
    })
    final_result.to_csv(r"z_neural_network.csv", index=None)

    # 这样可以是实现预测
    np.argmax(net(x1).data.numpy)
    test_y = net(x1)