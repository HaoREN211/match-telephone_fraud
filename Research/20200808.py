# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/8 9:41
# IDE：PyCharm

from Tools.data import get_train_test_data
from Features.rematch_features import RematchConfig
import pandas as pd

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()

    self = RematchConfig()
    temp_data = self.voc.copy()
    temp_data["hour"] = temp_data.apply(
        lambda x: 1 if ((int(x["start_datetime"][11:13])<6) or (int(x["start_datetime"][11:13])==23)) else 0, axis=1)

    # 夜间通话占比过高的用户，有效果但是有误伤。
    agg_data = temp_data.groupby("phone_no_m").agg(voc_cnt=("hour", pd.Series.count),
                                                   night_voc_cnt=("hour", pd.Series.sum))
    agg_data["night_voc_ratio"] = agg_data.apply(lambda x: round(x["night_voc_cnt"]/x["voc_cnt"], 4), axis=1)
    agg_data = self.user[["phone_no_m", "label"]].join(agg_data, on=["phone_no_m"]).fillna(0)
    agg_data[agg_data["night_voc_ratio"] > 0.6]["label"].value_counts()
    agg_data[agg_data["night_voc_ratio"] > 0.5]["label"].value_counts()
    print(agg_data[agg_data["night_voc_ratio"] > 0.6].reset_index()[["phone_no_m", "night_voc_ratio", "label"]])
    for current_phone in agg_data[agg_data["night_voc_ratio"] > 0.6]["phone_no_m"].values:
        print(current_phone)
    print(agg_data[agg_data["night_voc_ratio"] > 0.6].reset_index()[["phone_no_m", "night_voc_ratio", "label"]].loc[3, "phone_no_m"])

    # 夜间与多个用户进行过通话的用户
    night_voc = (temp_data[temp_data["hour"] == 1]
                 .groupby("phone_no_m")
                 .agg(night_voc_user_cnt = ("opposite_no_m", pd.Series.nunique)))
    night_voc = self.user[["phone_no_m", "label"]].join(night_voc, on=["phone_no_m"]).fillna(0)
    night_voc[night_voc["night_voc_user_cnt"]>5]["label"].value_counts()

