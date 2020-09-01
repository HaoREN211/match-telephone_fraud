# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/11 14:24
# IDE：PyCharm

from Tools.data import get_train_test_data
from Features.rematch_features import RematchConfig
import pandas as pd
from Tools.functions import best_ks

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()
    self = RematchConfig()

    # IMEI个数
    agg_data = self.voc.groupby("phone_no_m").agg(imei_cnt=("imei_m", pd.Series.nunique))
    temp_data = self.user[["phone_no_m", "label"]].join(agg_data, on=["phone_no_m"]).copy().fillna(0)

    temp_data[temp_data["imei_cnt"] == 0]["label"].value_counts()
    temp_data[temp_data["imei_cnt"] >= 2]["label"].value_counts()

    # 发送短信过于主动
    temp_data = self.sms[["phone_no_m", "opposite_no_m", "calltype_id"]].copy()
    temp_data["initiative"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
    temp_data["passive"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
    agg_data = (temp_data.groupby(["phone_no_m", "opposite_no_m"])
                .agg(initiative_cnt=("initiative", pd.Series.sum), passive_cnt=("passive", pd.Series.sum))
                .reset_index())
    agg_data["reactive_diff"] = agg_data.apply(lambda x: abs(x["initiative_cnt"]-x["passive_cnt"]), axis=1)
    result_data = (agg_data[agg_data["reactive_diff"] >= 20].groupby("phone_no_m")
                   .agg(user_cnt=("opposite_no_m", pd.Series.nunique))
                   .reset_index()
                   .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on="phone_no_m"))
    result_data["label"].value_counts()

    # 主动通话的通话记录中，持续联系天数在一天的用户数
    temp_data = self.voc[self.voc["calltype_id"] == 1][["phone_no_m", "opposite_no_m", "start_datetime"]].copy()
    temp_data["date"] = temp_data.apply(lambda x: x["start_datetime"][0:10], axis=1)

    agg_data = (temp_data.groupby(["phone_no_m", "opposite_no_m"])
                .agg(first_date=("date", pd.Series.min), last_date=("date", pd.Series.max))
                .reset_index())
    agg_data["one_day_contact"] = agg_data.apply(lambda x: 1 if x["first_date"]==x["last_date"] else 0, axis=1)

    result_data = self.user[["phone_no_m", "label"]].join(
        (agg_data.groupby("phone_no_m")
         .agg(user_cnt=("opposite_no_m", pd.Series.nunique),
              one_day_user_cnt=("one_day_contact", pd.Series.sum))), on=["phone_no_m"]).fillna(0)
    result_data["one_day_ratio"] = result_data.apply(lambda x: round(x["one_day_user_cnt"]/x["user_cnt"], 2)
                                                      if x["user_cnt"]>0 else 0, axis=1)
    bk = best_ks(result_data, "one_day_ratio", reverse=True)
    result_data[result_data["one_day_ratio"]>=0.87]["label"].value_counts()
