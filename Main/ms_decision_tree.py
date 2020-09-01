# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/13 15:02
# IDE：PyCharm

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


if __name__ == '__main__':
    columns = ['xgboost', 'random_forest', 'logistic_regression', 'svm']
    data_train = pd.read_excel("标签及分类.xlsx", sheet_name="训练集预测结果", header=0)
    data_test = pd.read_excel("标签及分类.xlsx", sheet_name="测试集预测结果", header=0)

    # 验证集成模型
    model = DecisionTreeClassifier()
    X, y = data_train[columns].copy(), data_train["label"].values
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)
    model.fit(train_X, train_y)
    val_y_predict = model.predict(val_X)
    print(accuracy_score(val_y, val_y_predict))

    # 预测
    test_X = data_test[columns].copy()
    model.fit(X, y)
    final_result = pd.DataFrame({
        "phone_no_m": data_test["phone_no_m"].values,
        "label": model.predict(test_X)
    })
    final_result.to_csv(r"zs_decision_tree.csv", index=None)

