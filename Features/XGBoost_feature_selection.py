# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/1 14:14
# IDE：PyCharm

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
from copy import copy


# 根据XGBoost特征的重要性筛选特征
def select_features(train_data, drop_columns, label_name, model=XGBClassifier(), cv=5):
    X = train_data.drop(columns=drop_columns)
    y = train_data[label_name].values

    model.fit(X, y)

    result = pd.DataFrame(columns=["threshold", "nb_feature", "accuracy_score"])
    for current_feature_importance in list(set(model.feature_importances_)):
        # 根据特征的重要性筛选特征
        selection = SelectFromModel(model, threshold=current_feature_importance, prefit=True)

        accuracy = 0
        # 划分训练集和验证集
        for i in range(cv):
            train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=i)
            select_train_X = selection.transform(train_X)

            # 训练数据
            selection_model = copy(model)
            selection_model.fit(select_train_X, train_y)

            # 验证结果
            select_val_X = selection.transform(val_X)
            val_y_predict = selection_model.predict(select_val_X)

            accuracy += accuracy_score(val_y, val_y_predict)

        result = result.append(
            pd.DataFrame({
            "threshold": [current_feature_importance]
            ,"accuracy_score": [accuracy/cv]
        }))

    result = result.sort_values(by=["accuracy_score"], ascending=False)

    # 获取验证集精确率最高的特征重要性，并根据此重要性筛选特征
    best_threshold = result.iloc[0,0]
    return list(X.columns[model.feature_importances_>=best_threshold])

