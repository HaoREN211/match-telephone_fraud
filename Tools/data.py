# @Time    : 2020/8/5 22:40
# @Author  : REN Hao
# @FileName: data.py
# @Software: PyCharm

import pandas as pd


# 获取训练集和测试集数据
def get_train_test_data():
    train_data, tmp_test_data = pd.read_excel("data_train.xlsx", header=0), pd.read_excel("data_test.xlsx", header=0)

    # 替换ARPU的缺失值
    none_index = tmp_test_data[tmp_test_data["arpu"] == "\\N"].index.to_list()
    if none_index:
        tmp_test_data.loc[none_index, "arpu"] = [0] * len(none_index)

    final_test_data = pd.DataFrame(columns=["phone_no_m", "label"])

    # 20200814添加，
    # 去除掉arpu为0的用户，直接做成规则
    print("去除掉arpu为0的用户，直接做成规则")
    train_data = train_data[train_data.apply(lambda x: False if x["arpu"] == 0 else True, axis=1)].copy()
    tmp_data = tmp_test_data[tmp_test_data["arpu"] == 0].copy()
    final_test_data = final_test_data.append(pd.DataFrame({
        "phone_no_m": tmp_data["phone_no_m"].values,
        "label": [1] * len(tmp_data)
    }))
    tmp_test_data = tmp_test_data[tmp_test_data.apply(lambda x: False if x["arpu"] == 0 else True, axis=1)].copy()

    # 20200817添加
    # 去除arpu大于等于550的用户，直接做成规则
    # 用户一小时内的通话数量中位数大于等于8 voc_inner_hour_cnt_median
    list_rules = [("arpu", 550),
                  # 20200818添加
                  ("voc_inner_hour_cnt_median", 8),
                  ("voc_inner_day_user_cnt_min", 30),
                  ("voc_imei_cnt", 9)
    ]
    for column_name, threshold in list_rules:
        print("去除"+column_name+"大于等于"+str(threshold)+"的用户，直接做成规则")
        train_data = train_data[train_data[column_name] < threshold]
        tmp_data = tmp_test_data[tmp_test_data[column_name] >= threshold].copy()
        final_test_data = final_test_data.append(pd.DataFrame({
            "phone_no_m": tmp_data["phone_no_m"].values,
            "label": [1] * len(tmp_data)
        }))
        tmp_test_data = tmp_test_data[tmp_test_data[column_name] < threshold]

    # 去除initiative_voc_user_cnt大于1275的用户，直接做成规则
    print("去除initiative_voc_user_cnt大于1275的用户，直接做成规则")
    train_data = train_data[train_data["initiative_voc_user_cnt"] <= 1275]
    tmp_data = tmp_test_data[tmp_test_data["initiative_voc_user_cnt"] > 1275].copy()
    final_test_data = final_test_data.append(pd.DataFrame({
        "phone_no_m": tmp_data["phone_no_m"].values,
        "label": [1] * len(tmp_data)
    }))
    tmp_test_data = tmp_test_data[tmp_test_data["initiative_voc_user_cnt"] <= 1275]

    # 去除voc_inner_day_user_cnt_max大于等于135的用户，直接做成规则
    print("去除voc_inner_day_user_cnt_max大于等于135的用户，直接做成规则")
    train_data = train_data[train_data["voc_inner_day_user_cnt_max"] < 135]
    tmp_data = tmp_test_data[tmp_test_data["voc_inner_day_user_cnt_max"] >= 135].copy()
    final_test_data = final_test_data.append(pd.DataFrame({
        "phone_no_m": tmp_data["phone_no_m"].values,
        "label": [1] * len(tmp_data)
    }))
    tmp_test_data = tmp_test_data[tmp_test_data["voc_inner_day_user_cnt_max"] < 135]

    # 命中高危APP的用户视为欺诈电话
    # print("命中高危APP的用户视为欺诈电话")
    # train_data = train_data[train_data["is_hit_rule_app"] == 0]
    # tmp_data = tmp_test_data[tmp_test_data["is_hit_rule_app"] == 1].copy()
    # final_test_data = final_test_data.append(pd.DataFrame({
    #     "phone_no_m": tmp_data["phone_no_m"].values,
    #     "label": [1] * len(tmp_data)
    # }))
    # tmp_test_data = tmp_test_data[tmp_test_data["is_hit_rule_app"] == 0]

    # 通话记录中去除高危电话列表
    # print("通话记录中去除高危电话列表")
    # column_name = "is_hit_rule_opposite"
    # train_data = train_data[train_data[column_name] == 0]
    # tmp_data = tmp_test_data[tmp_test_data[column_name] == 1].copy()
    # final_test_data = final_test_data.append(pd.DataFrame({
    #     "phone_no_m": tmp_data["phone_no_m"].values,
    #     "label": [1] * len(tmp_data)
    # }))
    # tmp_test_data = tmp_test_data[tmp_test_data[column_name] == 0]

    return train_data.reset_index(drop=True), tmp_test_data.reset_index(drop=True), final_test_data.reset_index(drop=True)
