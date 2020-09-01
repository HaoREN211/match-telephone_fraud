# @Time    : 2020/8/7 21:25
# @Author  : REN Hao
# @FileName: m_logistic.py
# @Software: PyCharm

from Tools.data import get_train_test_data
from Tools.feature_transforme import min_max_scale
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import toad
from Tools.functions import find_best_columns_by_correlation
from sklearn.model_selection import KFold
import pandas as pd
from sklearn.model_selection import train_test_split

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
    columns = find_best_columns_by_correlation(selected_data_tmp.drop(columns=["phone_no_m"]), "label", 0.1, 0.5)
    columns.insert(0, "label")
    columns.insert(0, "phone_no_m")
    selected_data = selected_data_tmp[columns].copy()

    # 交叉验证，对训练集中所有的样本进行预测。用于bagging聚合模型用
    kf = KFold(n_splits=10, shuffle=True, random_state=0)
    result_predict = pd.DataFrame(columns=["phone_no_m", "label"])
    for train_index, test_index in kf.split(train_data):
        temp_train_data, temp_test_data = selected_data.loc[train_index, :], selected_data.loc[test_index, :]
        temp_train_X, temp_train_y = temp_train_data.drop(columns=["phone_no_m", "label"]), temp_train_data["label"].values
        temp_test_X = temp_test_data.drop(columns=["phone_no_m", "label"])

        log_reg = LogisticRegression()
        log_reg.fit(temp_train_X, temp_train_y)

        result_predict = result_predict.append(pd.DataFrame({
            "phone_no_m": temp_test_data["phone_no_m"].values,
            "label": log_reg.predict(temp_test_X)
        }))
    result_predict.reset_index(drop=True, inplace=True)
    result_predict.to_excel("z_logistic_train.xlsx", index=None)

    # 验证预测结果
    result_predict.columns = ["phone_no_m", "label_predict"]
    result_predict = train_data[["phone_no_m", "label"]].join(result_predict.set_index("phone_no_m"), on="phone_no_m")
    print(accuracy_score(result_predict["label"].values.tolist(), result_predict["label_predict"].values.tolist()))

    # 将当前入模的特征保存下来，并存入本地文件
    df_columns = pd.DataFrame({"columns": columns})
    df_columns.to_excel("z_logistic_columns.xlsx", index=None)

    # 训练模型
    log_reg = LogisticRegression()

    # 验证模型
    train_X, val_X, train_y, val_y = train_test_split(selected_data.drop(columns=["phone_no_m", "label"]),
                                                      selected_data["label"].values, random_state=0)
    log_reg.fit(train_X, train_y)
    val_y_predict = log_reg.predict(val_X)
    print(accuracy_score(val_y, val_y_predict))

    log_reg.fit(selected_data.drop(columns=["phone_no_m", "label"]), selected_data["label"].values)

    # 预测
    new_test_data[selected_data.columns].drop(columns=["phone_no_m", "label"])
    y_test_predict = log_reg.predict(new_test_data[selected_data.columns].drop(columns=["phone_no_m", "label"]))
    final_result = final_test_data.append(pd.DataFrame({
        "phone_no_m": new_test_data["phone_no_m"].values,
        "label": y_test_predict
    }))
    final_result.to_csv("z_logistic_regression.csv", index=None)
