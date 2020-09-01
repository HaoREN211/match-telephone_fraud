# @Time    : 2020/7/31 21:50
# @Author  : REN Hao
# @FileName: app_about.py
# @Software: PyCharm
from Features.rematch_features import RematchConfig
from Tools.functions import *

# inside_data中同时安装了多个inside_app的用户
def two_same_application_user(inside_data, inside_app):
    inside_temp_data = inside_data[inside_data["busi_name"] == inside_app].copy()
    inside_temp_data = inside_temp_data.groupby(["phone_no_m", "busi_name"]).agg(same_app_cnt=("flow", pd.Series.count),
                                                                   label=("label", pd.Series.max)).reset_index()
    return set(inside_temp_data[inside_temp_data["same_app_cnt"] > 1]["phone_no_m"].values)

if __name__ == '__main__':
    self = RematchConfig()

    # 用户的app明细数据关联上用户的标签数据
    data = self.app.join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on="phone_no_m")

    # 安装量TOP的APP
    top_data = (data.groupby("busi_name")
                .agg(user_cnt=("label", pd.Series.count))
                .reset_index()
                .sort_values(by="user_cnt", ascending=False))

    # 判断黑白两类用户在某个APP上消费流量的差异
    compare_add_flow_diff(data, "微信", label="label")

    # 统计各APP的安装用户数和黑名单用户数
    data_sum = data.groupby(["busi_name"]).agg({
        "label": [pd.Series.sum, pd.Series.count],
    }).reset_index()
    data_sum.columns = ["app_name", "fake_user_cnt", "user_cnt"]

    # # 统计各APP的安装黑名单用户占比，并按照从高到低的比例进行排序
    data_sum["fake_ratio"] = data_sum.apply(
        lambda x: round(x["fake_user_cnt"]/x["user_cnt"], 4), axis=1)
    data_sum.sort_values(by=["fake_ratio"], ascending=False, inplace=True)
    data_sum.to_excel("app_check.xlsx", index=None)

    # 同时安装多个同款APP的标签分布情况
    temp_data = data.groupby(["phone_no_m", "busi_name"]).agg(same_app_cnt=("flow", pd.Series.count),
                                                              label=("label", pd.Series.max)).reset_index()
    temp_data = temp_data[temp_data["same_app_cnt"]>1].groupby("phone_no_m").agg(label=("label", pd.Series.max)).reset_index()
    temp_data["label"].value_counts()

    # 查看安装了“中国网络游戏服务网”的四个用户的APP列表，是否有其他的共性
    target_phone_no_m = list(data[data["busi_name"]=="中国网络游戏服务网"]["phone_no_m"].values)
    temp_data = data[data.apply(lambda x: True if x["phone_no_m"] in target_phone_no_m else False, axis=1)]
    temp_data = temp_data.groupby("busi_name").agg(user_cnt=("label", pd.Series.count)).reset_index().sort_values(by=["user_cnt"], ascending=False)

    # 同时安装了两个支付宝和两个微信的用户
    weixin = two_same_application_user(data, "微信")
    zhifubao = two_same_application_user(data, "支付宝")
    result = (pd.DataFrame({"phone_no_m": list(weixin.intersection(zhifubao))})
              .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]))
    result["label"].value_counts()

    # 用户安装APP数量和标签之间的关系
    temp_data = (data.groupby("phone_no_m")
                 .agg(app_cnt=("busi_name", pd.Series.count), app_dis_cnt=("busi_name", pd.Series.nunique))
                 .reset_index()
                 .join(self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"])
                 .copy())

    # 用户APP消费最大流量与标签之间的关系
    temp_data = data.groupby("phone_no_m").agg(max_flow=("flow", pd.Series.max), label=("label", pd.Series.max)).reset_index()
    temp_data.corr()
