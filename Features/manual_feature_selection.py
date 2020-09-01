# @Time    : 2020/7/29 22:29
# @Author  : REN Hao
# @FileName: manual_feature_selection.py
# @Software: PyCharm


# 手动分箱
def manual_feature_selection_20200729(data):
    result = data[["phone_no_m", "label"]].copy()

    # 发送短信天数过于活跃
    result["sms_activate_days_diff"] = data.apply(
        lambda x: 1 if x["sms_activate_days_diff"] > -9 else 0, axis=1)

    # 平均拨打电话间隔过短
    result["voc_interval_mean"] = data.apply(
        lambda x: 1 if x["voc_interval_mean"] < 5825 else 0, axis=1)

    # 与用户的通话天数过短
    result["voc_user_contact_days_mean"] = data.apply(
        lambda x: 1 if x["voc_user_contact_days_mean"] <= 1.9 else 0, axis=1)

    # 被呼占比过小
    result["passive_voc_ratio"] = data.apply(
        lambda x: 1 if x["passive_voc_ratio"] < 0.226 else 0, axis=1)

    # 主呼无归属城市
    result["initiative_voc_city_cnt"] = data.apply(
        lambda x: 1 if x["initiative_voc_city_cnt"] == 0 else 0, axis=1)

    # 用户关联身份证过多
    result["idcard_cnt"] = data.apply(
        lambda x: 1 if x["idcard_cnt"] >= 3 else 0, axis=1)

    result["high_voc_inner_day_user_cnt_max"] = data["high_voc_inner_day_user_cnt_max"].values

    # 与同一用户通话的最小次数过小
    result["voc_user_call_cnt_min"] = data.apply(
        lambda x: 1 if x["voc_user_call_cnt_min"] == 0 else 0, axis=1)

    # APP安装个数太少
    result["app_cnt"] = data.apply(
        lambda x: 1 if x["app_cnt"] == 0 else 0, axis=1)

    # 与同一用户被呼的最小次数过小
    result["passive_voc_user_call_cnt_median"] = data.apply(
        lambda x: 1 if x["passive_voc_user_call_cnt_median"] == 0 else 0, axis=1)

    # 与同一用户通话的最大次数过小
    result["voc_user_call_cnt_max"] = data.apply(
        lambda x: 1 if x["voc_user_call_cnt_max"] <= 5 else 0, axis=1)

    # 与同一用户主呼的最小次数过小
    result["initiative_voc_user_call_cnt_min"] = data.apply(
        lambda x: 1 if x["initiative_voc_user_call_cnt_min"] == 0 else 0, axis=1)

    result["initiative_voc_inner_day_dur_min"] = data.apply(
        lambda x: 1 if x["initiative_voc_inner_day_dur_min"] == 0 else 0, axis=1)

    result["passive_sms_inner_hour_cnt_min"] = data.apply(
        lambda x: 1 if x["passive_sms_inner_hour_cnt_min"] == 0 else 0, axis=1)

    # 同天内被呼持续时间过短
    result["passive_voc_inner_day_dur_max"] = data.apply(
        lambda x: 1 if x["passive_voc_inner_day_dur_max"] <= 39 else 0, axis=1)

    # 主呼占比过小
    result["initiative_voc_ratio"] = data.apply(
        lambda x: 1 if x["initiative_voc_ratio"] <= 0.0157 else 0, axis=1)

    result["voc_inner_hour_cnt_min"] = data.apply(
        lambda x: 1 if x["voc_inner_hour_cnt_min"] == 0 else 0, axis=1)

    result["passive_voc_inner_day_user_cnt_min"] = data.apply(
        lambda x: 1 if x["passive_voc_inner_day_user_cnt_min"] == 0 else 0, axis=1)

    # 接收短信数目过少
    result["passive_sms_cnt"] = data.apply(
        lambda x: 1 if x["passive_sms_cnt"] <= 37 else 0, axis=1)

    # 接收短信占比过少
    result["passive_sms_ratio"] = data.apply(
        lambda x: 1 if x["passive_sms_ratio"] <= 0.4357 else 0, axis=1)

    result["initiative_voc_interval_min"] = data.apply(
        lambda x: 1 if x["initiative_voc_interval_min"] <= 6 else 0, axis=1)

    return result
