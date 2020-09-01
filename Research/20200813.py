# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/13 15:23
# IDE：PyCharm

from Tools.data import get_train_test_data
from Tools.feature_transforme import min_max_scale
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import toad
from Tools.functions import find_best_columns_by_correlation
from sklearn.model_selection import KFold
import pandas as pd
from Tools.feature_selection import research_feature_by_forward_search, research_feature_by_backward_search

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()

    # 对数据进行归一化处理
    new_train_data, new_test_data = min_max_scale(train_data, test_data, exclude=["phone_no_m", "label"])

    # 下面以缺失率大于0.5.IV值小于0.05或者相关性大于0.9(保留较高的特征)来进行特征筛选。
    selected_data_tmp, drop_lst = toad.selection.select(new_train_data,
                                                        target='label', empty=0.5, iv=0.05, corr=0.7,
                                                        return_drop=True, exclude=['phone_no_m'])

    log_reg = LogisticRegression()
    columns = research_feature_by_forward_search(selected_data_tmp, [], model=log_reg)

    current_columns = selected_data_tmp.columns.tolist()
    for i in ["phone_no_m", "label"]:
        if i in current_columns:
            current_columns.pop(current_columns.index(i))
    columns = research_feature_by_backward_search(selected_data_tmp, current_columns)
    columns.insert(0, "label")
    columns.insert(0, "phone_no_m")
    selected_data = selected_data_tmp[columns].copy()

    # 交叉验证，对训练集中所有的样本进行预测。用于bagging聚合模型用
    kf = KFold(n_splits=10, shuffle=True, random_state=0)
    result_predict = pd.DataFrame(columns=["phone_no_m", "label"])
    for train_index, test_index in kf.split(train_data):
        temp_train_data, temp_test_data = selected_data.loc[train_index, :], selected_data.loc[test_index, :]
        temp_train_X, temp_train_y = temp_train_data.drop(columns=["phone_no_m", "label"]), temp_train_data[
            "label"].values
        temp_test_X = temp_test_data.drop(columns=["phone_no_m", "label"])

        log_reg = LogisticRegression()
        log_reg.fit(temp_train_X, temp_train_y)

        result_predict = result_predict.append(pd.DataFrame({
            "phone_no_m": temp_test_data["phone_no_m"].values,
            "label": log_reg.predict(temp_test_X)
        }))
    result_predict.reset_index(drop=True, inplace=True)
