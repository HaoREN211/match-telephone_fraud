# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/17 11:03
# IDE：PyCharm

from Tools.data import get_train_test_data
from Tools.feature_transforme import min_max_scale
import toad
from Tools.functions import find_best_columns_by_correlation
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data, final_test_data = get_train_test_data()

    # 对数据进行归一化处理
    new_train_data, new_test_data = min_max_scale(train_data, test_data, exclude=["phone_no_m", "label"])

    # 下面以缺失率大于0.5.IV值小于0.05或者相关性大于0.9(保留较高的特征)来进行特征筛选。
    selected_data_tmp, drop_lst = toad.selection.select(new_train_data,
                                                        target='label', empty=0.5, iv=0.05, corr=0.7,
                                                        return_drop=True, exclude=['phone_no_m'])

    # 筛选相关性大于0.1且特征之间相关性小于0.5的特征
    columns = find_best_columns_by_correlation(selected_data_tmp.drop(columns=["phone_no_m"]), "label", 0.1, 0.65)

    columns.insert(0, "label")
    columns.insert(0, "phone_no_m")
    selected_data = selected_data_tmp[columns].copy()

    # 划分训练集和验证集
    train_X, val_X, train_y, val_y = train_test_split(selected_data.drop(columns=["phone_no_m", "label"]),
                                                      selected_data["label"].values, random_state=0)
    rf0 = RandomForestClassifier(oob_score=True, random_state=12)

    # Lasso选择特征
    result = pd.DataFrame(columns=["accuracy", "columns"])
    for step in range(1, 100, 1):
        current_alpha = step*0.001
        print(current_alpha)
        # 训练模型
        lasso = Lasso(alpha=current_alpha)
        lasso.fit(train_X, train_y)
        current_columns = train_X.columns[[True if abs(x)>0 else False for x in lasso.coef_]].to_list()

        if current_columns:
            rf0.fit(train_X[current_columns], train_y)
            val_y_predict = rf0.predict(val_X[current_columns])

            result = result.append(pd.DataFrame({
                "accuracy": [accuracy_score(val_y, val_y_predict)],
                "columns": [current_columns]
            }))
    result.sort_values(by=["accuracy"], ascending=False).reset_index(drop=True, inplace=True)
    final_columns = result.loc[0, "columns"]

    rf0.fit(selected_data[final_columns], selected_data["label"].values)
    tmp_final_result = pd.DataFrame({"phone_no_m": new_test_data["phone_no_m"].values,
                                     "label": rf0.predict(new_test_data[final_columns])})
    final_result = tmp_final_result.append(final_test_data).reset_index(drop=True)
    final_result.to_csv("z_random_forest.csv", index=False)
