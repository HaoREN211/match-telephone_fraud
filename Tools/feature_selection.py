# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/30 9:56
# IDE：PyCharm

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from copy import copy
from xgboost import XGBClassifier
import pandas as pd
import numpy as np
from copy import copy

# 根据模型在测试集上的准确率验证模型的好坏程度
def estimate_model(X, y, model, cv=5):
    # n_splits 表示划分为几块（至少是2），默认是5
    # shuffle 表示是否打乱划分，默认False，即不打乱
    # random_state 表示是否固定随机起点，Used when shuffle == True.
    kf = KFold(n_splits=cv, shuffle=True, random_state=0)

    final_accuracy = 0
    for train_index, test_index in kf.split(X):
        # 划分训练集、测试集
        train_X, train_y, test_X, test_y = X.iloc[train_index, :], y[train_index], X.iloc[test_index, :], y[test_index]

        # 训练数据
        current_model = copy(model)
        current_model.fit(train_X, train_y)

        # 验证结果
        test_y_predict = current_model.predict(test_X)
        final_accuracy += accuracy_score(test_y, test_y_predict)

    return round(final_accuracy/cv, 4)

# 从NxD维数据集中寻找精准率最高的D-1维特征集合
def research_best_sub_features(X, y, model):
    print("--- 正在计算当前" + str(len(X)) + "X" + str(len(X.columns)) + "数据集的最优子特征集")

    result = pd.DataFrame(columns=["columns", "accuracy"])
    # 后向搜索，从当前N个特征的特征集合中去除掉一个特征，对每一个N-1子特征集合中寻找准确率最高的特征集合
    for current_column in X.columns:
        current_columns = copy(list(X.columns))
        current_columns.pop(list(X.columns).index(current_column))

        result = result.append(pd.DataFrame({
            "columns": [current_columns]
            ,"accuracy": [estimate_model(X[current_columns].copy(), y, model)]
        }))

    # 根据准确率从高到低的顺序将子特征集进行排序
    result = result.sort_values(by=["accuracy"], ascending=False).reset_index(drop=True)
    return result.loc[0, "accuracy"], result.loc[0, "columns"]

# 从NxD维数据集中寻找精准率最高的D+1维特征集合
def research_best_hyber_features(data, columns, model, label="label"):
    print("--- 正在计算当前" + str(len(columns)) + "X" + str(len(columns)) + "数据集的最优父特征集")
    result = pd.DataFrame(columns=["columns", "accuracy"])

    # 前搜索，从当前N个特征的特征集添加一个一个特征，对每一个N-1子特征集合中寻找准确率最高的特征集合
    for current_column in data.columns:
        if current_column in ["phone_no_m", "label"]:
            continue
        if current_column in columns:
            continue
        print("---合并"+current_column+"特征的数据进行探索")
        current_list_column = copy(columns)
        current_list_column.append(current_column)
        result = result.append(pd.DataFrame({
            "columns": [current_list_column]
            , "accuracy": [estimate_model(data[current_list_column].copy(), data[label].values, model)]
        }))

    # 根据准确率从高到低的顺序将子特征集进行排序
    result = result.sort_values(by=["accuracy"], ascending=False).reset_index(drop=True)
    return result.loc[0, "accuracy"], result.loc[0, "columns"]

# 通过后向搜索寻找准确率最高的子特征集合
def research_feature_by_backward_search(data, columns, label="label", drop_columns=None, model=XGBClassifier()):
    if len(columns) == 1:
        return columns

    # 将训练数据集中的ID和标签去除掉
    drop_columns = ["label", "phone_no_m"] if drop_columns is None else drop_columns
    X, y = data.drop(columns=drop_columns)[columns], data[label].values

    # 计算当前特征集合的准确率和最优N-1子特征集合的准确率
    current_accuracy = estimate_model(X, y, model)
    sub_accuracy, sub_columns = research_best_sub_features(X, y, model)

    if sub_accuracy >= current_accuracy:
        # N-1子特征集合的最优准确率高于当前特征集合的准确率，进行子特征集合的子特征集合搜索
        print("找到当前最优子特征集合，进行下一步拆解")
        return research_feature_by_backward_search(
            data, sub_columns, model=model, label=label, drop_columns=drop_columns)
    else:
        # N-1子特征集合的最优准确率低于当前特征集合的准确率，则停止搜索。返回当前结果。
        print("当前无最优子特征集合，返回当前特征")
        return X.columns

# 通过前向搜索寻找准确率最高的父特征集合
def research_feature_by_forward_search(data, columns, label="label", drop_columns=None, model=XGBClassifier()):
    # 当前的最优特征集合已经是全量集合，停止寻找。
    if len(columns) == np.shape([data])[1]-2:
        return columns

    # 将训练数据集中的ID和标签去除掉
    drop_columns = ["label", "phone_no_m"] if drop_columns is None else drop_columns
    X, y = data.drop(columns=drop_columns)[columns], data[label].values

    # 计算当前特征集合的准确率和最优N-1子特征集合的准确率
    current_accuracy = 0 if len(columns) == 0 else estimate_model(X, y, model)
    hyber_accuracy, hyber_columns = research_best_hyber_features(data, columns, model, label="label")

    if hyber_accuracy >= current_accuracy:
        # N+1父特征集合的最优准确率高于当前特征集合的准确率，进行父特征集合的父特征集合搜索
        print("找到当前最优父特征集合，进行下一步合并")
        return research_feature_by_forward_search(
            data, hyber_columns, model=model, label=label, drop_columns=drop_columns)
    else:
        # N+1父特征集合的最优准确率低于当前特征集合的准确率，则停止搜索。返回当前结果。
        print("当前无最优父特征集合，返回当前特征")
        return columns

# 结合前向搜索和后向搜索进行对特征的筛选
def research_feature_by_forward_backward_search(data, columns, label="label", drop_columns=None, model=XGBClassifier()):
    # 将训练数据集中的ID和标签去除掉
    drop_columns = ["label", "phone_no_m"] if drop_columns is None else drop_columns
    X, y = data.drop(columns=drop_columns), data[label].values

    # 计算当前特征集合的准确率和最优N-1子特征集合的准确率
    final_accuracy = 0 if len(columns) == 0 else estimate_model(X, y, model)
    is_fin = False

    while not is_fin:
        is_fin = True

        # 前向搜索
        current_accuracy, current_columns = research_best_hyber_features(data, columns, model=model, label=label)
        if current_accuracy > final_accuracy:
            final_accuracy = copy(current_accuracy)
            columns = copy(current_columns)
            is_fin = False

        # 后向搜索
        if len(columns) > 1:
            current_accuracy, current_columns = research_best_sub_features(X[columns], y, model)
            if current_accuracy > final_accuracy:
                final_accuracy = copy(current_accuracy)
                columns = copy(current_columns)
                is_fin = False
        print("当前特征数量为："+str(len(columns)))

    return columns



