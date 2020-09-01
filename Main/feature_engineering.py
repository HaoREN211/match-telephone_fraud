# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/2 10:53
# IDE：PyCharm

from Main import *
from Tools.functions import *

def feature_engineering():
    self = Config()

    data = self.get_voc_opposite_user_cnt()

    print("正在加工通话人数相关特征。。。")
    data = data.join(self.get_voc_user_max_min_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工同天内通话人数相关特征。。。")
    data = data.join(self.get_voc_user_inner_day().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工同天内通话次数相关特征相关特征。。。")
    data = data.join(self.get_voc_cnt_inner_day().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工与同一用户的平均通话次数相关特征。。。")
    data = data.join(self.get_user_avg_voc_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工用户各呼叫类型的呼叫次数相关特征。。。")
    data = (data.join(self.get_voc_call_type_id().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])
            .drop(columns=["call_cnt", "calltype_id"]))

    print("正在加工身份证下电话号码个数相关特征。。。")
    temp_data = self.train_user[["phone_no_m", "idcard_cnt", "arpu_202005"]].copy()
    temp_data.columns = ["phone_no_m", "idcard_cnt", "arpu"]
    data = data.join(temp_data.set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工短信相关特征。。。")
    temp_data = self.get_sms_cnt()
    temp_data.columns = ['phone_no_m', 'label', 'sms_cnt', 'calltype_id', 'sms_type_1_cnt',
       'sms_type_2_cnt', 'call_cnt', 'sms_type_1_ratio', 'sms_type_2_ratio']
    temp_data = temp_data[['phone_no_m', 'sms_cnt', 'sms_type_1_cnt', 'sms_type_2_cnt', 'sms_type_1_ratio', 'sms_type_2_ratio']]
    data = data.join(temp_data.set_index("phone_no_m"), on=["phone_no_m"])

    print("正在加工app数量特征。。。")
    data = (data.join(self.app_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]))

    print("正在加工app流量特征。。。")
    data = (data.join(self.flow_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]))

    print("正在加工高危app特征。。。")
    high_risk_app = pd.read_excel(r"high_risk_app.xlsx", header=0)
    high_risk_app = high_risk_app[high_risk_app["fake_ratio"] >= 0.6][["busi_name", "fake_ratio"]].drop_duplicates().copy()
    temp_data = (self.train_app[["phone_no_m", "busi_name"]]
                 .join(high_risk_app.set_index("busi_name"), on=["busi_name"])
                 .dropna(subset=["fake_ratio"]).groupby(["phone_no_m"]).max())
    data = data.join(temp_data[["fake_ratio"]], on=["phone_no_m"]).fillna(0)
    data["fake_ratio"] = data.apply(lambda x: 1 if x["fake_ratio"] > 0 else 0, axis=1)

    print("正在加工白名单APP数量特征。。。")
    data = (data.join(self.get_white_black_app_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]))
    data["black_app_ratio"] = data.apply(lambda x: x["black_app_cnt"] / x["app_cnt"] if x["app_cnt"] > 0 else 0, axis=1)
    data["white_app_ratio"] = data.apply(lambda x: x["white_app_cnt"] / x["app_cnt"] if x["app_cnt"] > 0 else 0, axis=1)

    print("正在加工活跃天数APP数量特征。。。")
    data = data.join(self.active_days().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工拨打城市数量特征。。。")
    data = data.join(self.call_city_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工拨打间隔时间特征。。。")
    data = data.join(self.call_interval_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工主动拨打间隔时间特征。。。")
    data = data.join(self.initiative_call_interval_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工给用户发送的平均短信个数。。。")
    data = data.join(self.avg_sms_type_1_cnt_per_interval().drop(columns=["label"]).set_index("phone_no_m"),
                     on=["phone_no_m"]).fillna(0)

    print("正在加工imei个数。。。")
    data = data.join(self.voc_imei_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工各通话类型的区域个数。。。")
    data = data.join(self.county_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工通话时长的相关特征。。。")
    data = data.join(self.voc_dur_info().drop(columns=["label", "active_days"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print("正在加工通话时长的相关特征。。。")
    data = data.join(self.multiple_sms_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.initiative_passive_activate_days_diff().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.interactive_user_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    data = data.join(self.same_user_call_time_last().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    # 20200707新增
    calculate_iv_by_split_box_by_frequency(data, "voc_cnt", 4)
    data["voc_cnt_class"] = get_split_box_label(data, "voc_cnt", 4)
    data["voc_user_mean_cnt_class"] = get_split_box_label(data, "voc_user_mean_cnt", 4)
    data["voc_user_cnt_class"] = get_split_box_label(data, "voc_user_cnt", 4)
    data["call_type_1_cnt_class"] = get_split_box_label(data, "call_type_1_cnt", 4)
    data["call_type_2_cnt_class"] = get_split_box_label(data, "call_type_2_cnt", 5)
    data["sms_cnt_class"] = get_split_box_label(data, "sms_cnt", 4)
    data["sms_type_2_cnt_class"] = get_split_box_label(data, "sms_type_2_cnt", 4)
    data["flow_class"] = get_split_box_label(data, "flow", 6)
    data["active_days_class"] = get_split_box_label(data, "active_days", 4)

    temp_data = self.call_high_risk_opposite()
    data = data.join(temp_data.drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    temp_data = self.sms_high_risk_opposite()
    data = data.join(temp_data.drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    print(data.corr()["label"])

    # 202020708新增特征
    data = data.join(self.call_user_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.initiative_call_user_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.initiative_call_user_ratio().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.passive_call_user_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    data = data.join(self.passive_call_user_ratio().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    # 20200710新增特征
    data = data.join(self.user_imei_user_cnt().drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)

    return data
