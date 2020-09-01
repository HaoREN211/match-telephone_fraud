# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/10 9:58
# IDE：PyCharm

from Tools.data import get_train_test_data
from Features.rematch_features import RematchConfig
import pandas as pd

def contact_cnt_verify(contact_cnt):
    global agg_data
    tmp_data = agg_data[agg_data["contact_cnt"] >= contact_cnt].groupby("phone_no_m").agg(label=("label", pd.Series.max))
    print(tmp_data["label"].value_counts())
    return tmp_data["label"].value_counts()

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()

    self = RematchConfig()

    # 标签与微信流量之间的关系
    temp_data = self.app[self.app["busi_name"] == "微信"].copy()
    temp_data = (self.user[["phone_no_m", "label"]]
                 .join(self.app[self.app["busi_name"] == "微信"].drop(columns=["month_id", "busi_name"]).set_index("phone_no_m"), on=["phone_no_m"])
                 .fillna(0).copy())
    # 单纯看微信流量和标签之间的相关性，没有任何相关性。
    temp_data.corr()
    # 1967个好用户、1939个坏用户没有安装微信
    temp_data[temp_data["flow"] == 0]["label"].value_counts()

    # 安装app的个数
    temp_data = self.app.groupby("phone_no_m").agg(app_cnt=("busi_name", pd.Series.nunique))
    temp_data = self.user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0).copy()
    # 1757个坏用户、1000个好用户没有安装APP
    temp_data[temp_data["app_cnt"] == 0]["label"].value_counts()

    temp_data[temp_data["flow"] > 2000]["label"].value_counts()

    # 当天与同一个用户有交互
    temp_data = self.voc[['phone_no_m', 'opposite_no_m', 'calltype_id', 'start_datetime']].copy()
    temp_data.columns = ['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']
    temp_data = temp_data.append(self.sms.copy())

    temp_data["date"] = temp_data.apply(lambda x: x["request_datetime"][0:10], axis=1)
    temp_data["initiative"] = temp_data.apply(lambda x: 1 if x["calltype_id"]==1 else 0, axis=1)
    temp_data["passive"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
    self.sms.columns

    agg_data = (temp_data.groupby(
        ["phone_no_m", "opposite_no_m", "date"]).agg(max_initiative=("initiative", pd.Series.max),
                                                     max_passive=("passive", pd.Series.max))
                .reset_index())
    # 同天中，一个用户与另外一个用户同时有呼叫和被叫的记录
    agg_data["interactive"] = agg_data.apply(lambda x: 1 if ((x["max_initiative"]==1) and (x["max_passive"]==1)) else 0, axis=1)
    agg_data = agg_data.groupby("phone_no_m").agg(interactive_cnt=("interactive", pd.Series.sum))
    agg_data = self.user[["phone_no_m", "label"]].join(agg_data, on=["phone_no_m"]).fillna(0).copy()

    # 没有安装微信的用户
    temp_data = self.app[['phone_no_m', 'busi_name']].copy()
    temp_data["has_we_chat"] = temp_data.apply(lambda x: 1 if x["busi_name"]=="微信" else 0, axis=1)
    temp_data = temp_data.groupby("phone_no_m").agg(has_we_chat=("has_we_chat", pd.Series.max))
    temp_data = self.user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0).copy()
    temp_data[temp_data["has_we_chat"] == 1]["label"].value_counts()
    temp_data[temp_data["has_we_chat"] == 0]["label"].value_counts()

    temp_data[(temp_data["has_we_chat"] == 0) & (temp_data["label"] == 0)]["phone_no_m"].values[0]

    # 标签与谷歌应用流量之间的关系
    temp_data = (self.user[["phone_no_m", "label"]]
                 .join(
        self.app[self.app["busi_name"] == "谷歌应用"].drop(columns=["month_id", "busi_name"]).set_index("phone_no_m"),
        on=["phone_no_m"])
                 .fillna(0).copy())
    # 单纯看微信流量和标签之间的相关性，没有任何相关性。
    temp_data.corr()
    # 1967个好用户、1939个坏用户没有安装微信
    temp_data[temp_data["flow"] == 0]["label"].value_counts()


    # 最大通话时长
    temp_data = self.voc[["phone_no_m", "call_dur"]].groupby("phone_no_m").agg(max_dur=("call_dur", pd.Series.max)).copy()
    temp_data = self.user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0)

    # 同天与同一个用户主动通讯过多，凝似骚扰电话
    temp_voc = self.voc[self.voc["calltype_id"] == 1][['phone_no_m', 'opposite_no_m', 'start_datetime']].copy()
    temp_voc.columns = ['phone_no_m', 'opposite_no_m', 'request_datetime']
    temp_data = temp_voc.append(self.sms[self.sms["calltype_id"] == 1][['phone_no_m', 'opposite_no_m', 'request_datetime']].copy())
    temp_data["date"] = temp_data.apply(lambda x: x["request_datetime"][0:10], axis=1)
    temp_data.drop_duplicates(inplace=True)
    agg_data = (temp_data.groupby(['phone_no_m', 'opposite_no_m', 'date'])
                .agg(concact_cnt=("request_datetime", pd.Series.count))
                .reset_index()
                .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]))



    # 同天与同一个用户通讯过多，且对方无回复，凝似骚扰电话
    temp_voc = self.voc[['phone_no_m', 'opposite_no_m', 'calltype_id', 'start_datetime']].copy()
    temp_voc.columns = ['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']
    temp_data = temp_voc.append(
        self.sms[['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']].copy())
    temp_data.drop_duplicates(inplace=True)
    # temp_data = self.sms[['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']].drop_duplicates().copy()
    temp_data["date"] = temp_data.apply(lambda x: x["request_datetime"][0:10], axis=1)
    temp_data["initiative"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
    temp_data["passive"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)

    agg_data = (temp_data.groupby(['phone_no_m', 'opposite_no_m', 'date'])
                .agg(initiative_cnt=("initiative", pd.Series.sum),
                     passive_cnt=("passive", pd.Series.sum))
                .reset_index()
                .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]))
    agg_data["contact_cnt"] = agg_data.apply(lambda x: x["initiative_cnt"]-x["passive_cnt"], axis=1)

    contact_cnt = 10
    tmp_data = agg_data[(agg_data["contact_cnt"] >= contact_cnt) & (agg_data["label"]==0)].groupby("phone_no_m").agg(
        label=("label", pd.Series.max))
    set(agg_data[(agg_data["contact_cnt"] >= contact_cnt) & (agg_data["label"] == 0)]["phone_no_m"].values)

    # 短时间与同一个用户发送短信过多，且对方无回复，凝似骚扰短信
    temp_data = self.sms[['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']].drop_duplicates().copy()
    temp_data["date"] = temp_data.apply(lambda x: x["request_datetime"][0:13], axis=1)
    temp_data["initiative"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
    temp_data["passive"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
    agg_data = (temp_data.groupby(['phone_no_m', 'opposite_no_m', 'date'])
                .agg(initiative_cnt=("initiative", pd.Series.sum),
                     passive_cnt=("passive", pd.Series.sum))
                .reset_index()
                .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]))
    agg_data["contact_cnt"] = agg_data.apply(lambda x: x["initiative_cnt"] - x["passive_cnt"], axis=1)

    # 归属地为空的通话占比
    temp_data = self.voc[["phone_no_m", "city_name"]].copy()
    temp_data["nan_city_name"] = temp_data.apply(lambda x: 1 if pd.isna(x["city_name"]) else 0, axis=1)
    agg_data = temp_data.groupby(["phone_no_m"]).agg(
        nan_city_name_cnt = ("nan_city_name", pd.Series.sum),
        voc_cnt = ("nan_city_name", pd.Series.count)
    )
    agg_data["nan_city_name_ratio"] = agg_data.apply(lambda x: x["nan_city_name_cnt"]/x["voc_cnt"], axis=1)
    agg_data = self.user[["phone_no_m", "label"]].join(agg_data, on=["phone_no_m"]).fillna(0)
    agg_data[(agg_data["nan_city_name_ratio"] == 1) & (agg_data["label"]==0)]["phone_no_m"].values[0]
    agg_data.corr()["label"]

    # 一分钟内与同一个用户发送短信过多，且对方无回复，凝似骚扰短信
    temp_data = self.sms[['phone_no_m', 'opposite_no_m', 'calltype_id', 'request_datetime']].drop_duplicates().copy()
    temp_data["date"] = temp_data.apply(lambda x: x["request_datetime"][0:18], axis=1)
    temp_data["initiative"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
    temp_data["passive"] = temp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)

    agg_data = (temp_data.groupby(['phone_no_m', 'opposite_no_m', 'date'])
                .agg(sms_cnt=("calltype_id", pd.Series.count),
                     initiative_cnt=("initiative", pd.Series.sum),
                     passive_cnt=("passive", pd.Series.sum))
                .reset_index())
    label_data = self.user[["phone_no_m", "label"]].join(agg_data.set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
    agg_label_data = label_data.groupby("phone_no_m").agg(max_sms_cnt=("sms_cnt", pd.Series.max),
                                         mean_sms_cnt=("sms_cnt", pd.Series.mean),
                                         label=("label", pd.Series.max))

    tmp_data = label_data[label_data["sms_cnt"] >= 2].groupby("phone_no_m").agg(label=("label", pd.Series.max),
                                                                                user_cnt=("opposite_no_m", pd.Series.nunique),
                                                                                cnt=("sms_cnt", pd.Series.count))

    temp_data = self.user[["phone_no_m", "label"]].join(temp_data.set_index("phone_no_m"), on=["phone_no_m"])
    agg_data = (temp_data.groupby(["phone_no_m", "opposite_no_m", "date"])
                .agg(initiative_cnt=("initiative", pd.Series.sum),
                     passive_cnt=("passive", pd.Series.sum),
                     label=("label", pd.Series.max))
                .reset_index())
    agg_data["contact_cnt"] = agg_data.apply(lambda x: x["initiative_cnt"]-x["passive_cnt"], axis=1)
    tmp_data = agg_data[agg_data["contact_cnt"] >= 2].groupby("phone_no_m").agg(label=("label", pd.Series.max),
                                                                                user_cnt=("opposite_no_m", pd.Series.nunique),
                                                                                cnt=("contact_cnt", pd.Series.count))


