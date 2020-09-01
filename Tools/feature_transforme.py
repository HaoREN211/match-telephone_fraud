# @Time    : 2020/8/7 21:33
# @Author  : REN Hao
# @FileName: feature_transforme.py
# @Software: PyCharm
from sklearn.preprocessing import MinMaxScaler


# 将训练集数据、测试集数据进行归一化处理
def min_max_scale(train_data, test_data, exclude=None):
    # 默认不归一化手机号码和标签
    if exclude is None:
        exclude = ["phone_no_m", "label"]

    # 合并训练集、测试集数据。用于后面的特征归一化处理
    train_data["is_train"], test_data["is_train"] = [1] * len(train_data), [0] * len(test_data)
    data = train_data.append(test_data).reset_index(drop=True)

    # 筛选要归一化的特征列表
    columns = list(data.columns)
    for column_to_drop in exclude:
        if column_to_drop in columns:
            columns.pop(columns.index(column_to_drop))

    # 对数据进行归一化处理
    mm = MinMaxScaler()
    data.loc[:, columns] = mm.fit_transform(data.loc[:, columns])

    return (data[data["is_train"] == 1].drop(columns=["is_train"]).copy(),
            data[data["is_train"] == 0].drop(columns=["is_train"]).copy())
