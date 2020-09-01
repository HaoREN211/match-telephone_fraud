# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/12 10:23
# IDE：PyCharm

from Tools.data import get_train_test_data
from Features.rematch_features import RematchConfig
import pandas as pd
from Tools.functions import best_ks

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()
    self = RematchConfig()

    # APP安装数量。验证app安装数量为0的用户是否都有问题。
    self.data[["app_cnt", "label"]].corr()
    temp_data = self.data[["app_cnt", "label"]].copy()
    temp_data["has_no_app"] = temp_data.apply(lambda x: 1 if x["app_cnt"] == 0 else 0, axis=1)
    temp_data[temp_data["has_no_app"] == 1]["label"].value_counts()

    self.data["has_no_app"] = temp_data.apply(lambda x: 1 if x["app_cnt"] == 0 else 0, axis=1)

    # 同一时刻和同一用户在不同地方进行通话？
    temp_data = self.voc[["phone_no_m", "opposite_no_m", "start_datetime", "county_name"]].copy()
    agg_data = temp_data.groupby(["phone_no_m", "opposite_no_m", "start_datetime"]).agg(
        voc_cnt=("county_name", pd.Series.count),
        county_cnt=("county_name", pd.Series.nunique)
    )
    problem_phone = list(set(agg_data[agg_data["county_cnt"] > 1].reset_index()["phone_no_m"].values))
    tmp_data = self.user[["phone_no_m", "label"]].copy()
    tmp_data["problem_county_user"] = tmp_data.apply(lambda x: 1 if x["phone_no_m"] in problem_phone else 0, axis=1)
    tmp_data[tmp_data["problem_county_user"] == 1]["label"].value_counts()

    # 微信流量异常和微信软件个数异常
    temp_data = self.app[self.app["busi_name"] == "微信"][["phone_no_m", "flow"]].copy()
    temp_data = temp_data.groupby("phone_no_m").agg(flow=("flow", pd.Series.sum),
                                                    nb_we_chat=("flow", pd.Series.count))

    result_data = self.user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0)
    temp_data.groupby("phone_no_m").agg(record=("flow", pd.Series.count)).sort_values(by=["record"], ascending=False)

    # 最后活跃时间
    temp_data = self.voc[["phone_no_m", "start_datetime"]].copy()
    temp_data["voc_last_day"] = temp_data.apply(lambda x: int(x["start_datetime"][8:10]),
                                                axis=1)
    agg_data = self.user[["phone_no_m", "label"]].join(temp_data.groupby("phone_no_m")
                                                       .agg(last_day=("voc_last_day", pd.Series.max)),
                                                       on=["phone_no_m"]).fillna(0)
    agg_data[agg_data["last_day"] <= 2]["label"].value_counts()
    bk = best_ks(agg_data, "last_day", reverse=False)

    # 最后活跃日期在24日及之前
    agg_data["last_active_day_too_early"] = agg_data.apply(
        lambda x: 1 if x["last_day"] <= 24 else 0, axis=1)

    # 关联身份证过多
    temp_data = self.user[["idcard_cnt", "label"]].copy()
    bk = best_ks(temp_data, "idcard_cnt", reverse=True)

    # 被呼平均通话时长
    temp_data = self.voc[self.voc["calltype_id"] == 2][["phone_no_m", "call_dur"]].copy()
    agg_data = self.user[["phone_no_m", "label"]].join(temp_data.groupby("phone_no_m").agg(
        passive_voc_dur_mean=("call_dur", pd.Series.mean)
    ), on=["phone_no_m"]).fillna(0)
    bk = best_ks(agg_data, "passive_voc_dur_mean", reverse=False)
    agg_data["passive_dur_too_low"] = agg_data.apply(
        lambda x: 1 if x["passive_voc_dur_mean"] <= 18 else 0, axis=1
    )
    agg_data.corr()

    # 通话记录中出现的区域数量
    temp_data = self.voc[["phone_no_m", "county_name"]].drop_duplicates().copy()
    agg_data = self.user[["phone_no_m", "label"]].join(
        temp_data.groupby("phone_no_m").agg(county_cnt=("county_name", pd.Series.nunique)), on=["phone_no_m"]).fillna(0)
    agg_data[agg_data["county_cnt"] == 0]["label"].value_counts()

    bs = best_ks(self.data, "initiative_voc_user_cnt", reverse=True)
    bs[bs["ks"]==max(bs["ks"].values)]
