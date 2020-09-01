# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/11 10:38
# IDE：PyCharm

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

if __name__ == '__main__':
    train_data = pd.read_excel("data_train.xlsx", header=0)
    test_data = pd.read_excel("data_test.xlsx", header=0)

    X, y, test_X = train_data.drop(columns=["phone_no_m", "label"]), train_data["label"].values, test_data.drop(columns=["phone_no_m", "label"])
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0, test_size=1/4)

    # 训练模型
    dt_model = DecisionTreeClassifier(max_depth=2)
    dt_model.fit(train_X, train_y)
    dt_model.fit(X, y)

    plt.figure(figsize=(15, 9))
    plot_tree(dt_model, filled=True,
              feature_names=X.columns)
    plt.show()