# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2020/6/30 11:03
# IDE：PyCharm

import numpy as np
import datetime as dt
import time
import math
import pandas as pd
from Features.XGBoost_feature_selection import *


# 调出phone_no_m用户的通话记录、短信记录、app记录
def generate_target_data(data, phone_no_m):
    data_user = data.user[data.user["phone_no_m"] == phone_no_m].copy()
    data_voc = data.voc[data.voc["phone_no_m"] == phone_no_m].copy().sort_values(by=["start_datetime"],
                                                                                 ascending=True)
    data_sms = data.sms[data.sms["phone_no_m"] == phone_no_m].copy().sort_values(by=["request_datetime"],
                                                                                 ascending=True)
    data_app = data.app[data.app["phone_no_m"] == phone_no_m].copy().sort_values(by=["flow"],
                                                                                 ascending=False)
    with pd.ExcelWriter('target'+phone_no_m+'.xlsx') as writer:
        data_user.to_excel(writer, sheet_name="user", index=None)
        data_voc.to_excel(writer, sheet_name="voc", index=None)
        data_sms.to_excel(writer, sheet_name="sms", index=None)
        data_app.to_excel(writer, sheet_name="app", index=None)


# 判断不同类型用户在某个app流量上的差异
def compare_add_flow_diff(data, app_name, label="label"):
    sub_data = data[data["busi_name"] == app_name].copy()
    return compare_distribution(sub_data, "flow", label=label)


# 判断column特征在不同label下的分布差异
def compare_distribution(data, column, label="label"):
    label_values = set(data[label].values)
    result = pd.DataFrame()

    for current_label_value in label_values:
        result["label_"+str(current_label_value)] = data[data[label]==current_label_value].describe().loc[:, column]
    return result


# best_ks分箱
def best_ks(data, column, label="label", reverse=False):
    column_value = sorted(list(set(data[column].values)), reverse=reverse)

    # 数据集中所有好样本和坏样本的总和
    bad_all, good_all = len(data[data[label]==1]), len(data[data[label]==0])

    # 当前坏样本和好样本的积累数量
    cur_bad, cur_good = 0, 0

    result = pd.DataFrame(columns=["value", "cur_good", "cur_bad", "cur_good_ratio", "cur_bad_ratio", "ks"])
    for current_value in column_value:
        sub_data = data[data[column] == current_value].copy()
        bad, good = len(sub_data[sub_data[label]==1]), len(sub_data[sub_data[label]==0])
        cur_bad += bad
        cur_good += good
        result = result.append(pd.DataFrame({"value": [current_value], "cur_good": [cur_good], "cur_bad": [cur_bad],
                                    "cur_good_ratio": [round(cur_good / good_all, 3)],
                                    "cur_bad_ratio": [round(cur_bad / bad_all, 3)],
                                    "ks": [round(cur_bad / bad_all, 3)-round(cur_good / good_all, 3)]}))
    result = result.reset_index()
    result.drop(columns=["index"], inplace=True)
    return result


# 计算所有特征的所有区间相关的GINI系数
def calculate_all_column_interval_gini(data, label="label"):
    for column in data.columns:
        if column in ["phone_no_m", "label"]:
            continue
        print("---正在计算"+column+"相关的基尼系数")
        result = calculate_gini_interval(data, column, label=label)
        result.to_excel("Gini/"+column+".xlsx", index=None)


# 计算数据集data中column的基尼系数
def calculate_gini(data, column, label="label"):
    result = float(0)
    list_column_values = list(set(data[column].values))
    list_label_values = list(set(data[label].values))
    for current_column_value in list_column_values:
        sub_data = data[data[column] == current_column_value].copy()
        sub_data_len = len(sub_data)
        current_result = float(1)
        for current_label_value in list_label_values:
            possibility = float(len(sub_data[sub_data[label] == current_label_value])) / float(sub_data_len)
            current_result -= possibility ** 2
        result += float(sub_data_len) * current_result / float(len(data))
    return result


# 计算特征column所有分区的基尼系数
def calculate_gini_interval(data, column, label="label"):
    temp_data = data[[column, label]].copy()
    result = pd.DataFrame(columns=["column", "min_value", "max_value", "bad_sample_cnt","gini"])
    for v_min, v_max in column_all_intervals(data=data, column=column):
        temp_data["test_label"] = temp_data.apply(lambda x: 1 if v_min<=x[column]<=v_max else 0, axis=1)
        result = result.append(pd.DataFrame({
            "column": [column], "min_value": [v_min], "max_value": [v_max],
            "bad_sample_cnt": [sum(temp_data["test_label"].values)], "gini": calculate_gini(temp_data, "test_label", label)
        }))
    return result


# 获取数据集中所有的数据分区
def column_all_intervals(data, column):
    column_values = list(set(data[column].values))
    result = []
    for index_i, value_i in enumerate(column_values):
        for value_j in column_values[index_i:]:
            result.append((value_i, value_j))
    return result


# 获取数据集两两的列对
def column_pair(data):
    columns = data.columns
    result = []
    for index_i, value_i in enumerate(columns):
        for value_j in columns[index_i + 1:]:
            result.append((value_i, value_j))
    return result


# 计算组合过后的列的gini值
def column_pair_gini(data):
    swap_columns = ["phone_no_m", "label"]
    column_value_threshold = 20
    result = pd.DataFrame(columns=["column_1", "column_1_min", "column_1_max",
                                   "column_2", "column_2_min", "column_2_max", "gini"])
    for column_i, column_j in column_pair(data):
        if column_i in swap_columns or column_j in swap_columns:
            continue
        if len(set(data[column_i].values)) > column_value_threshold or len(
                set(data[column_j].values)) > column_value_threshold:
            continue
        sub_result = pd.DataFrame(columns=["column_1", "column_1_min", "column_1_max",
                                           "column_2", "column_2_min", "column_2_max", "gini"])
        print("--- 当前正在计算"+str(column_j)+" <-> "+str(column_i)+"的组合最小GINI数")
        for v_i_min, v_i_max in column_all_intervals(data, column_i):
            for v_j_min, v_j_max in column_all_intervals(data, column_j):
                data["test_label"] = data.apply(lambda x: 1 if ((v_i_min <= x[column_i] <= v_i_max)
                                                                and (v_j_min <= x[column_j] <= v_j_max)) else 0, axis=1)
                current_gini = calculate_gini(data, "test_label")
                sub_result = sub_result.append(pd.DataFrame(
                    {"column_1": [column_i], "column_1_min": [v_i_min], "column_1_max": [v_i_max],
                     "column_2": [column_j], "column_2_min": [v_j_min], "column_2_max": [v_j_max],
                     "gini": [current_gini]}))
        sub_result.sort_values(by=["gini"], ascending=True, inplace=True)
        result = result.append(sub_result.iloc[0, :], ignore_index=True)
        break
    return result


# 将datetime格式的字符串转化为date格式的字符串
def convert_datetime_to_date(x, column_name=None):
    if column_name:
        return x[column_name][0:10] if len(x[column_name]) == 19 else None
    return x[0:10] if len(x) == 19 else None


# SELECT COUNT(DISTINCT column) FROM data GROUP BY key
def func_count_distinct(data, key, column):
    return data.groupby(key).agg({column: pd.Series.nunique})


# SELECT COUNT(column) FROM data GROUP BY key
def func_count(data, key, column):
    return data.groupby(key).agg({column: pd.Series.count})


# SELECT SUM(column) FROM data GROUP BY key
def func_sum(data, key, column):
    return data.groupby(key).agg({column: pd.Series.sum})


# 根据相关系数筛选入模的特征
def find_best_columns_by_correlation(data, label, threshold_filtration, threshold_inter):
    """
    根据相关系数筛选入模的特征
    :param data: 加工好的数据集
    :param label: 标签的列名
    :param threshold_filtration: 如果当前特征与标签的相关系数小于等于threshold_filtration则过滤该特征
    :param threshold_inter: 如果该特征与已选特征的相关性太高，则不建议入模，舍弃掉
    :return:
    """
    list_columns = []
    all_correlation = data.corr()
    correlation = pd.DataFrame({"column": all_correlation[label].index, "corr": list(all_correlation[label])})
    correlation["corr_abs"] = correlation.apply(lambda x: abs(x["corr"]), axis=1)
    correlation.sort_values(by=["corr_abs"], ascending=False, inplace=True)

    for row in correlation.itertuples():
        current_column, current_corr_abs = getattr(row, "column"), getattr(row, "corr_abs")
        if current_column == label:
            continue
        # 如果当前特征与标签的相关系数小于等于threshold_filtration则过滤该特征
        if current_corr_abs <= threshold_filtration:
            continue
        # 如果该特征与已选特征的相关性太高，则不建议入模，舍弃掉
        has_inter_corr = False
        for current_inter_column in list_columns:
            if abs(all_correlation.loc[current_inter_column, current_column]) >= threshold_inter:
                has_inter_corr = True
                break
        if not has_inter_corr:
            list_columns.append(current_column)
    return list_columns


# 验证模型的准确率
def verify_model_accuracy(model, data, columns, label, cv=5):
    X, y = data[columns], data[label].values
    accuracy_scores = 0
    for i in range(cv):
        train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=i)
        model.fit(train_X, train_y)
        val_y_predict = model.predict(val_X)
        accuracy_scores += accuracy_score(val_y, val_y_predict)
    return accuracy_scores / cv


# 根据要分箱的数目，计算相应的iv值
def calculate_iv_by_split_box_by_frequency(data, column, nb, label="label"):
    percentile = split_box_by_frequency(data, column, nb)
    percentile[-1] = percentile[-1] + 1
    return calculate_iv_by_percentile(data, column, percentile, label)


# 根据要分箱的箱数，确定分箱之后的值
def get_split_box_label(data, column, nb):
    percentile = split_box_by_frequency(data, column, nb)
    percentile[-1] = percentile[-1] + 1
    return data[[column]].apply(lambda x: get_percentile_label(x[column], percentile), axis=1)


# 计算好坏样本在data数据集中的样本数
def calculate_good_bad(data, label):
    return len(data[data[label] == 0]), len(data[data[label] == 1])


# 等频分箱
def split_box_by_frequency(data, column, nb):
    temp_result = []
    temp_interval = (100 / nb)
    for i in range(nb):
        temp_result.append(int(i * temp_interval))
    temp_result.append(100)
    percentile = [int(x) for x in np.percentile(data[column].values, temp_result)]
    percentile[-1] = percentile[-1] + 1
    return percentile


# 根据给定的分箱边界计算分箱后特征的iv值
def calculate_iv_by_percentile(data, column, percentile, label):
    data["class"] = data[[column]].apply(lambda x: get_percentile_label(x[column], percentile), axis=1)
    return calculate_iv(data, "class", label)


# 计算离散变量column的iv值
def calculate_iv(data, column, label):
    result_iv = 0
    nb_good, nb_bad = calculate_good_bad(data, label)
    temp_result = calculate_woe_detail(data, column, label)
    for current_row in temp_result.itertuples():
        current_value, current_woe = getattr(current_row, "value"), getattr(current_row, "woe")
        current_data = data[data[column] == current_value][[column, label]]
        current_good, current_bad = calculate_good_bad(current_data, label)
        result_iv += ((current_bad / nb_bad) - (current_good / nb_good)) * current_woe
    return result_iv


# 根据给定的分箱边界分箱
def get_percentile_label(x, percentile):
    current_label = -1
    for index in range(len(percentile) - 1):
        current_label += 1
        if percentile[index] <= x < percentile[index + 1]:
            return current_label
    return -1


def calculate_woe_detail(data, column, label):
    nb_good, nb_bad = calculate_good_bad(data, label)
    list_value = set(data[column].values)
    final_result = pd.DataFrame(columns=["value", "woe"])
    for current_value in list_value:
        current_data = data[data[column] == current_value][[column, label]]
        current_good, current_bad = calculate_good_bad(current_data, label)
        if current_good == 0 and current_bad == 0:
            result = 0
        elif current_bad == 0:
            result = -100
        elif current_good == 0:
            result = 100
        else:
            result = (current_bad / nb_bad) / (current_good / nb_good)
            result = math.log(result, math.e)
        final_result = final_result.append(pd.DataFrame({"value": [current_value],
                                                         "woe": [result]}))
    # final_result.to_excel("WOE/"+column+".xlsx")
    return final_result


# 计算判定认为为短时间通话的时间间隔下，用户的短时间通话占比
def find_short_call_dur(train_voc, train_user, threshold_call_dur):
    """
    :param train_voc: 用户的通话记录
    :param train_user: 用户属性
    :param threshold_call_dur: 认定为短时间通话的通话时间
    :return:
    """
    call_cnt = train_voc[train_voc["calltype_id"] == 1][["phone_no_m", "call_dur"]].groupby(
        ["phone_no_m"]).count()
    call_cnt.columns = ["call_cnt"]

    short_call_cnt = train_voc[(train_voc["calltype_id"] == 1) & (train_voc["call_dur"] <= threshold_call_dur)][
        ["phone_no_m", "call_dur"]].groupby(["phone_no_m"]).count()
    short_call_cnt.columns = ["short_call_cnt"]

    data = train_user[["phone_no_m", "label"]].join(call_cnt, on=["phone_no_m"]).join(short_call_cnt,
                                                                                      on=["phone_no_m"])
    data["short_call_ratio"] = data.apply(lambda x: x["short_call_cnt"] / x["call_cnt"] if x["call_cnt"] > 0 else 0,
                                          axis=1)
    data = data.fillna(0)
    return data.corr()["label"]


# 计算通话间隔时间的最小值最大值、平均值、中位数、方差
def calculate_interval(train_voc, train_user, column_name):
    tmp_data = train_voc.copy()

    # 将通话开始时间转化为datetime类型
    tmp_data["datetime"] = train_voc.apply(lambda x: dt.datetime.strptime(x["start_datetime"], "%Y-%m-%d %H:%M:%S"),
                                           axis=1)
    # 根据通话开始时间和通话间隔，计算通话结束时间
    tmp_data["end_datetime"] = tmp_data.apply(lambda x: x["datetime"] + dt.timedelta(seconds=x["call_dur"]), axis=1)
    # 将通话开始时间转化成为时间戳
    tmp_data["start_timestamp"] = tmp_data.apply(lambda x: int(time.mktime(x["datetime"].timetuple())), axis=1)

    # 将每个人的通话记录按照通话开始时间进行排序
    tmp_data_rank = tmp_data.groupby("phone_no_m")["start_timestamp"].rank(ascending=True)
    tmp_data["rank"] = [int(x) for x in tmp_data_rank]
    tmp_data["next_rank"] = tmp_data.apply(lambda x: x["rank"] + 1, axis=1)

    tmp_data_next = tmp_data[["phone_no_m", "rank", "datetime"]].copy()
    merge_data = tmp_data[["phone_no_m", "next_rank", "end_datetime"]].join(
        tmp_data_next.set_index(["phone_no_m", "rank"]), on=["phone_no_m", "next_rank"])

    # 计算用户相邻两次通话的通话间隔
    merge_data = merge_data.dropna(subset=["datetime"])
    merge_data["call_interval"] = merge_data.apply(lambda x: (x["datetime"] - x["end_datetime"]).seconds, axis=1)

    final_result = merge_data[["phone_no_m", "call_interval"]].groupby("phone_no_m").agg(
        [np.min, np.max, np.mean, np.median, np.std])
    final_result.columns = column_name
    final_result = train_user[["phone_no_m", "label"]].join(final_result, on=["phone_no_m"]).fillna(0)
    return final_result


# 分箱
def split_box(data_set, feature_name, label_name, find_down=True, include_0=False):
    list_feature = list(np.unique([int(x) for x in data_set[feature_name].values]))
    if list_feature[0] == 0:
        if not include_0:
            list_feature.pop(0)

    result = pd.DataFrame(columns=["threshold", "iv"])

    for current_threshold in list_feature:

        nb_bad, nb_good = len(data_set[data_set[label_name] == 1]), len(data_set[data_set[label_name] == 0])

        if find_down:
            if include_0:
                target_subset = data_set[(data_set[feature_name] >= 0) & (data_set[feature_name] <= current_threshold)]
            else:
                target_subset = data_set[(data_set[feature_name] > 0) & (data_set[feature_name] <= current_threshold)]
        else:
            target_subset = data_set[data_set[feature_name] >= current_threshold]

        nb_c_bad, nb_c_good = len(target_subset[target_subset[label_name] == 1]), len(
            target_subset[target_subset[label_name] == 0])

        if nb_c_bad == 0 or nb_c_good == 0:
            current_iv = 1
        else:
            current_iv = (nb_c_bad / nb_bad - nb_c_good / nb_good) * math.log(
                (nb_c_bad / nb_bad) / (nb_c_good / nb_good), math.e)
        result = result.append(pd.DataFrame({"threshold": [current_threshold],
                                             "iv": [current_iv]}))
    return result


# 根据时间段内发送短信的用户数，评定风险等级
def avg_sms_type_1_user_per_interval_class_define(x):
    if x >= 29:
        return 4
    elif x >= 4:
        return 3
    elif x >= 2:
        return 2
    else:
        return 0
