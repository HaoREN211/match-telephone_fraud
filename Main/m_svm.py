# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/12 9:32
# IDE：PyCharm

from Tools.data import get_train_test_data
from Tools.feature_transforme import min_max_scale
from Tools.functions import find_best_columns_by_correlation
import toad
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import pandas as pd

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data, final_test_data = get_train_test_data()

    # 对数据进行归一化处理
    new_train_data, new_test_data = min_max_scale(train_data, test_data, exclude=["phone_no_m", "label"])

    # 下面以缺失率大于0.5.IV值小于0.05或者相关性大于0.9(保留较高的特征)来进行特征筛选。
    selected_data, drop_lst = toad.selection.select(new_train_data,
                                                    target='label', empty=0.5, iv=0.05, corr=0.7,
                                                    return_drop=True, exclude=['phone_no_m'])

    # 筛选相关性大于0.1且特征之间相关性小于0.5的特征
    columns = find_best_columns_by_correlation(selected_data.drop(columns=["phone_no_m"]), "label", 0.1, 0.65)

    # 将当前入模的特征保存下来，并存入本地文件
    df_columns = pd.DataFrame({"columns": columns})
    df_columns.to_excel("z_svm_columns.xlsx", index=None)

    model = svm.SVC(C=1.0, kernel='rbf', gamma='auto', decision_function_shape='ovr', cache_size=500)

    # 验证模型的好坏
    train_X, val_X, train_y, val_y = train_test_split(selected_data[columns], selected_data["label"].values, random_state=0)
    model.fit(train_X, train_y)
    val_y_predict = model.predict(val_X)
    print("精确度为："+str(round(accuracy_score(val_y, val_y_predict), 3)))

    columns.insert(0, "label")
    columns.insert(0, "phone_no_m")

    # 交叉验证，对训练集中所有的样本进行预测。用于bagging聚合模型用
    kf = KFold(n_splits=10, shuffle=True, random_state=0)
    result_predict = pd.DataFrame(columns=["phone_no_m", "label"])
    for train_index, test_index in kf.split(train_data):
        temp_train_data, temp_test_data = selected_data.loc[train_index, columns], selected_data.loc[test_index, columns]
        temp_train_X, temp_train_y = temp_train_data.drop(columns=["phone_no_m", "label"]), temp_train_data[
            "label"].values
        temp_test_X = temp_test_data.drop(columns=["phone_no_m", "label"])

        svm_model = svm.SVC(C=1.0, kernel='rbf', gamma='auto', decision_function_shape='ovr', cache_size=500)
        svm_model.fit(temp_train_X, temp_train_y)

        result_predict = result_predict.append(pd.DataFrame({
            "phone_no_m": temp_test_data["phone_no_m"].values,
            "label": svm_model.predict(temp_test_X)
        }))
    result_predict.reset_index(drop=True, inplace=True)
    result_predict.to_excel("z_svm_train.xlsx", index=None)

    # 预测
    model = svm.SVC(C=1.0, kernel='rbf', gamma='auto', decision_function_shape='ovr', cache_size=500)
    model.fit(new_train_data.loc[:, columns].drop(columns=["phone_no_m", "label"]), new_train_data["label"].values)
    final_result = final_test_data.append(pd.DataFrame({
        "phone_no_m": test_data["phone_no_m"].values,
        "label": model.predict(new_test_data.loc[:, columns].drop(columns=["phone_no_m", "label"]))
    }))
    final_result.to_csv(r"z_svm.csv", index=None)
