# @Time    : 2020/6/17 20:16
# @Author  : REN Hao
# @FileName: __init__.py.py
# @Software: PyCharm

import os
from Tools.functions import *


class Config(object):
    ROOT_PATH = os.getcwd().split("match-telephone_fraud")[0]
    TRAIN_DATA_DIR = os.path.join(ROOT_PATH, r"match-telephone_fraud\Data\Train")
    FILTRATION_TRAIN_DATA_DIR = os.path.join(ROOT_PATH, r"match-telephone_fraud\Data\filtration_train")
    TEST_DATA_DIR = os.path.join(ROOT_PATH, r"match-telephone_fraud\Data\Test")
    REMATCH_DATA_DIR = os.path.join(ROOT_PATH, r"match-telephone_fraud\Data\rematch")

    def load_data(self, type=0):
        """
        :param type: type=0: 训练集；type=1：四月测试集；type=2：五月测试集
        :param is_train:
        :param is_rematch:
        :return:
        """
        if type==0:
            self.train_user = self.get_train_user()
            self.train_voc = self.get_train_voc()
            self.train_sms = self.get_train_sms()
            self.train_app = self.get_train_app()
        elif type==1:
            self.train_user = self.get_test_user()
            self.train_voc = self.get_test_voc()
            self.train_sms = self.get_test_sms()
            self.train_app = self.get_test_app()
        else:
            self.train_user = self.get_rematch_user()
            self.train_voc = self.get_rematch_voc()
            self.train_sms = self.get_rematch_sms()
            self.train_app = self.get_rematch_app()
        self.data = self.train_user[["phone_no_m", "label"]]

    # 通话记录中用户数量
    def call_user_cnt(self):
        if "call_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "call_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "call_user_cnt", "label"]]

    # 用户关联过的imei关联的用户数总和
    def user_imei_user_cnt(self):
        user_cnt = self.imei_user_cnt()
        temp_data = (self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "imei_m"]].drop_duplicates()
                     .join(user_cnt.set_index(["imei_m"]), on=["imei_m"])
                     .groupby(["phone_no_m"]).sum())
        temp_data.columns = ["user_imei_user_cnt"]
        final_data = self.train_user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0)
        return final_data


    # iemi关联的用户数
    def imei_user_cnt(self):
        initiative_user_cnt = self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "imei_m"]].drop_duplicates()
        passive_user_cnt = self.train_voc[self.train_voc["calltype_id"]==2][["opposite_no_m", "imei_m"]].drop_duplicates()
        passive_user_cnt.columns=["phone_no_m", "imei_m"]
        user_cnt = initiative_user_cnt.append(passive_user_cnt).drop_duplicates()
        user_cnt = user_cnt.groupby(["imei_m"]).count().reset_index()
        user_cnt.columns = ["imei_m", "imei_user_cnt"]
        return user_cnt

    # 主呼中用户数量
    def initiative_call_user_cnt(self):
        if "initiative_call_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[self.train_voc["calltype_id"]==1][['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "initiative_call_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "initiative_call_user_cnt", "label"]]

    # 主呼中用户数量占通话记录中用户数量的比例
    def initiative_call_user_ratio(self):
        if "initiative_call_user_ratio" not in self.data.columns:
            self.call_user_cnt()
            self.initiative_call_user_cnt()
            self.data["initiative_call_user_ratio"] = (self.data[["initiative_call_user_cnt", "call_user_cnt"]]
                                                       .apply(lambda x: x["initiative_call_user_cnt"]/x["call_user_cnt"]
                                                              if x["call_user_cnt"]>0 else 0, axis=1))
        return self.data[["phone_no_m", "initiative_call_user_ratio", "label"]]

    # 被呼中用户数量
    def passive_call_user_cnt(self):
        if "passive_call_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[self.train_voc["calltype_id"] == 2][['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "passive_call_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "passive_call_user_cnt", "label"]]

    # 被呼中用户数量占通话记录中用户数量的比例
    def passive_call_user_ratio(self):
        if "passive_call_user_ratio" not in self.data.columns:
            self.call_user_cnt()
            self.passive_call_user_cnt()
            self.data["passive_call_user_ratio"] = (self.data[["passive_call_user_cnt", "call_user_cnt"]]
                                                       .apply(lambda x: x["passive_call_user_cnt"] / x["call_user_cnt"]
                                                            if x["call_user_cnt"] > 0 else 0, axis=1))
        return self.data[["phone_no_m", "passive_call_user_ratio", "label"]]

    # 主呼通话记录中的人数除以被呼通话记录中的人数
    def initiative_passive_user_ratio(self):
        if "initiative_passive_user_ratio" not in self.data.columns:
            self.passive_call_user_cnt()
            self.initiative_call_user_cnt()
            self.data["initiative_passive_user_ratio"] = (self.data[["initiative_call_user_cnt", "passive_call_user_cnt"]]
                .apply(lambda x: x["initiative_call_user_cnt"] / x["passive_call_user_cnt"]
                    if x["passive_call_user_cnt"] > 0 else 0, axis=1))
        return self.data[["phone_no_m", "initiative_passive_user_ratio", "label"]]

    # 呼转中用户数量
    def turn_call_user_cnt(self):
        if "turn_call_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[self.train_voc["calltype_id"] == 3][['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "turn_call_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "turn_call_user_cnt", "label"]]

    # 呼转中用户数量占通话记录中用户数量的比例
    def turn_call_user_ratio(self):
        if "turn_call_user_ratio" not in self.data.columns:
            self.call_user_cnt()
            self.turn_call_user_cnt()
            self.data["turn_call_user_ratio"] = (self.data[["turn_call_user_cnt", "call_user_cnt"]]
                                                       .apply(lambda x: x["turn_call_user_cnt"] / x["call_user_cnt"]
                                                            if x["call_user_cnt"] > 0 else 0, axis=1))
        return self.data[["phone_no_m", "turn_call_user_ratio", "label"]]

    # 短信记录中用户数量
    def sms_user_cnt(self):
        if "sms_user_cnt" not in self.data.columns:
            tmp_data = (self.train_sms[['phone_no_m', 'opposite_no_m']].drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "sms_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "sms_user_cnt", "label"]]

    # 发送短信记录中用户数量
    def initiative_sms_user_cnt(self):
        if "initiative_sms_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[self.train_sms["calltype_id"] == 1][['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "initiative_sms_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "initiative_sms_user_cnt", "label"]]

    # 发送短信记录中用户数量占短信记录中用户数量的比例
    def initiative_sms_user_ratio(self):
        if "initiative_sms_user_ratio" not in self.data.columns:
            self.sms_user_cnt()
            self.initiative_sms_user_cnt()
            self.data["initiative_sms_user_ratio"] = (self.data[["initiative_sms_user_cnt", "sms_user_cnt"]]
                                                       .apply(
                lambda x: x["initiative_sms_user_cnt"] / x["sms_user_cnt"]
                if x["sms_user_cnt"] > 0 else 0, axis=1))
        return self.data[["phone_no_m", "initiative_sms_user_ratio", "label"]]

    # 接收短信记录中用户数量
    def passive_sms_user_cnt(self):
        if "passive_sms_user_cnt" not in self.data.columns:
            tmp_data = (self.train_voc[self.train_sms["calltype_id"] == 2][['phone_no_m', 'opposite_no_m']]
                        .drop_duplicates().groupby(["phone_no_m"]).count().reset_index())
            tmp_data.columns = ["phone_no_m", "passive_sms_user_cnt"]
            self.data = self.data.join(tmp_data.set_index(['phone_no_m']), on=["phone_no_m"]).fillna(0)
        return self.data[["phone_no_m", "passive_sms_user_cnt", "label"]]

    # 接收短信记录中用户数量占短信记录中用户数量的比例
    def passive_sms_user_ratio(self):
        if "passive_sms_user_ratio" not in self.data.columns:
            self.sms_user_cnt()
            self.passive_sms_user_cnt()
            self.data["passive_sms_user_ratio"] = (self.data[["passive_sms_user_cnt", "sms_user_cnt"]]
                .apply(
                lambda x: x["passive_sms_user_cnt"] / x["sms_user_cnt"]
                if x["sms_user_cnt"] > 0 else 0, axis=1))
        return self.data[["phone_no_m", "passive_sms_user_ratio", "label"]]


    def generate_high_risk_opposite(self):
        temp_data = self.train_voc[['phone_no_m', 'opposite_no_m']].drop_duplicates()
        temp_data = temp_data.join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"])
        temp_data["user_cnt"] = [1] * len(temp_data)
        temp_data = temp_data.groupby(["opposite_no_m"]).sum().reset_index()
        temp_data["call_fake_ratio"] = temp_data.apply(lambda x: x["label"]/x["user_cnt"], axis=1)
        temp_data.to_excel("call_opposite_no_m.xlsx", index=None)

        temp_data = self.train_sms[['phone_no_m', 'opposite_no_m']].drop_duplicates()
        temp_data = temp_data.join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"])
        temp_data["user_cnt"] = [1] * len(temp_data)
        temp_data = temp_data.groupby(["opposite_no_m"]).sum().reset_index()
        temp_data["call_fake_ratio"] = temp_data.apply(lambda x: x["label"] / x["user_cnt"], axis=1)
        temp_data.to_excel("sms_opposite_no_m.xlsx", index=None)

    def call_high_risk_opposite(self):
        high_risk_opposite = pd.read_excel("call_opposite_no_m.xlsx")
        high_risk_opposite = high_risk_opposite[(high_risk_opposite["call_fake_ratio"] == 1) & (high_risk_opposite["user_cnt"] > 2)]["opposite_no_m"].values
        temp_data = self.train_voc[["phone_no_m", "opposite_no_m"]].copy()
        temp_data["call_high_risk_opposite_cnt"] = temp_data.apply(lambda x: 1 if x["opposite_no_m"] in high_risk_opposite else 0, axis=1)
        temp_data = temp_data[["phone_no_m", "call_high_risk_opposite_cnt"]].groupby(["phone_no_m"]).sum().reset_index()
        temp_data["call_high_risk_opposite_label"] = temp_data.apply(lambda x: 1 if x["call_high_risk_opposite_cnt"]>0 else 0, axis=1)
        return self.train_user[["phone_no_m", "label"]].join(temp_data.set_index(["phone_no_m"]), on=["phone_no_m"])

    def sms_high_risk_opposite(self):
        high_risk_opposite = pd.read_excel("sms_opposite_no_m.xlsx")
        high_risk_opposite = high_risk_opposite[(high_risk_opposite["call_fake_ratio"] == 1) & (high_risk_opposite["user_cnt"] > 2)]["opposite_no_m"].values
        temp_data = self.train_sms[["phone_no_m", "opposite_no_m"]].copy()
        temp_data["sms_high_risk_opposite_cnt"] = temp_data.apply(lambda x: 1 if x["opposite_no_m"] in high_risk_opposite else 0, axis=1)
        temp_data = temp_data[["phone_no_m", "sms_high_risk_opposite_cnt"]].groupby(["phone_no_m"]).sum().reset_index()
        temp_data["sms_high_risk_opposite_label"] = temp_data.apply(lambda x: 1 if x["sms_high_risk_opposite_cnt"]>0 else 0, axis=1)
        return self.train_user[["phone_no_m", "label"]].join(temp_data.set_index(["phone_no_m"]), on=["phone_no_m"])


    # 统计用户在每个城市拨打的电话次数总和
    def passive_call_per_city(self):
        temp_date = self.train_voc[self.train_voc["calltype_id"] == 1][["phone_no_m", "city_name", "imei_m"]].groupby(
            ["phone_no_m", "city_name"]).count().reset_index()
        temp_date.columns = ["phone_no_m", "call_city_name", "call_cnt"]
        return temp_date

    # 找到拨打电话次数最频繁的所在市
    def passive_call_rank_1_city(self):
        temp_date = self.passive_call_per_city()
        temp_date["rank"] = [int(x) for x in temp_date.groupby(["phone_no_m"])["call_cnt"].rank(ascending=False)]
        return temp_date[temp_date["rank"] == 1][["phone_no_m", "call_city_name"]]


    # 用户拨打电话最频繁所在的市不是用户的开户市
    def call_city_is_not_default(self):
        if "call_city_is_not_default" not in self.data.columns:
            temp_date = self.passive_call_rank_1_city()
            result = (self.train_user[["phone_no_m", "city_name"]]
                      .join(temp_date.set_index("phone_no_m"), on=["phone_no_m"])
                      .dropna(subset=["call_city_name"]))
            result["call_city_is_not_default"] = result.apply(lambda x: 1 if x["city_name"]!=x["call_city_name"] else 0, axis=1)
            result = (self.train_user[["phone_no_m", "label"]]
                      .join(result[["phone_no_m", "call_city_is_not_default"]].set_index("phone_no_m"), on=["phone_no_m"])
                      .fillna(0))
            result.corr()
            calculate_iv(result, "call_city_is_not_default", "label")
            self.data = self.data.join(result[["phone_no_m", "call_city_is_not_default"]].set_index(["phone_no_m"]),
                                       on=["phone_no_m"])
        return self.data[["phone_no_m", "call_city_is_not_default", "label"]]


    # 与用户的通话总时长
    def same_user_total_duration(self):
        temp_data = self.train_voc[["phone_no_m", "opposite_no_m", "call_dur"]].groupby(["phone_no_m", "opposite_no_m"]).sum().reset_index()
        temp_data = temp_data[["phone_no_m", "call_dur"]].groupby(["phone_no_m"]).agg([np.min, np.max, np.mean, np.median, np.std])
        temp_data.columns = ["user_duration_min", "user_duration_max", "user_duration_mean", "user_duration_median", "user_duration_std"]
        final_result = self.train_user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"])
        print(final_result.corr()["label"])
        return final_result


    # 与用户的通话持续天数
    def same_user_call_time_last(self):
        temp_data = self.train_voc[["phone_no_m", "opposite_no_m", "start_datetime"]].copy()
        temp_data["date"] = temp_data.apply(lambda x: x["start_datetime"][0:10], axis=1)

        agg_result = temp_data[["phone_no_m", "opposite_no_m", "date"]].groupby(["phone_no_m", "opposite_no_m"]).agg([np.max, np.min]).reset_index()
        agg_result.columns = ["phone_no_m", "opposite_no_m", "last_date", "first_date"]
        agg_result["duration_days"] = agg_result.apply(lambda x: (dt.datetime.strptime(x["last_date"], "%Y-%m-%d")-dt.datetime.strptime(x["first_date"], "%Y-%m-%d")).days+1, axis=1)

        final_result = agg_result[["phone_no_m", "duration_days"]].groupby(["phone_no_m"]).agg([np.min, np.max, np.mean, np.median, np.std])
        final_result.columns = ["duration_days_min", "duration_days_max", "duration_days_mean", "duration_days_median", "duration_days_std"]
        final_result = self.train_user[["phone_no_m", "label"]].join(final_result, on=["phone_no_m"])
        print(final_result.corr()["label"])
        return final_result


    # 用户最耗流量app分析
    def user_most_flow_app(self):
        tmp_data = self.train_app[["phone_no_m", "busi_name", "flow"]].copy()
        tmp_data["app_rank"] = [ int(x) for x in tmp_data.groupby(["phone_no_m"])["flow"].rank(ascending=False)]
        tmp_data = tmp_data[tmp_data["app_rank"]==1]
        tmp_data = tmp_data.join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"])
        tmp_data["user_cnt"] = [1]*len(tmp_data)

        result = tmp_data[["busi_name", "label", "user_cnt"]].groupby(["busi_name"]).sum().reset_index()
        result["fake_ratio"] = result.apply(lambda x: x["label"]/x["user_cnt"], axis=1)


    # 通话记录中同时有发送和接受短信或拨打和接听的用户数和用户占比
    def interactive_user_cnt(self):
        # 通话相关
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m", "calltype_id"]].drop_duplicates().copy()

        # 统计用户通话记录中出现的用户数
        voc_user = tmp_data[["phone_no_m", "opposite_no_m"]].drop_duplicates()
        voc_user_cnt = voc_user.groupby(["phone_no_m"]).count()
        voc_user_cnt.columns = ["call_user_cnt"]

        initiative_voc_user = tmp_data[tmp_data["calltype_id"] == 1][["phone_no_m", "opposite_no_m"]].drop_duplicates()
        initiative_voc_user["initiative_voc_label"] = [1]*len(initiative_voc_user)
        passive_voc_user = tmp_data[tmp_data["calltype_id"] == 2][["phone_no_m", "opposite_no_m"]].drop_duplicates()
        passive_voc_user["passive_voc_user"] = [1] * len(passive_voc_user)
        result_voc = (voc_user.join(initiative_voc_user.set_index(["phone_no_m", "opposite_no_m"]), on=["phone_no_m", "opposite_no_m"])
                      .join(passive_voc_user.set_index(["phone_no_m", "opposite_no_m"]), on=["phone_no_m", "opposite_no_m"]).fillna(0))
        result_voc["interactive_call_user_cnt"] = result_voc.apply(lambda x: 1 if (x["initiative_voc_label"]==1 and x["passive_voc_user"]==1) else 0, axis=1)
        result_voc = result_voc[["phone_no_m", "interactive_call_user_cnt"]].groupby(["phone_no_m"]).sum()

        # 短信相关
        tmp_data = self.train_sms[["phone_no_m", "opposite_no_m", "calltype_id"]].drop_duplicates().copy()

        # 统计用户短信记录中出现的用户数
        sms_user = tmp_data[["phone_no_m", "opposite_no_m"]].drop_duplicates()
        sms_user_cnt = sms_user.groupby(["phone_no_m"]).count()
        sms_user_cnt.columns = ["sms_user_cnt"]

        initiative_sms_user = tmp_data[tmp_data["calltype_id"] == 1][["phone_no_m", "opposite_no_m"]].drop_duplicates()
        initiative_sms_user["initiative_sms_label"] = [1] * len(initiative_sms_user)
        passive_sms_user = tmp_data[tmp_data["calltype_id"] == 2][["phone_no_m", "opposite_no_m"]].drop_duplicates()
        passive_sms_user["passive_sms_label"] = [1] * len(passive_sms_user)
        result_sms = (sms_user.join(initiative_sms_user.set_index(["phone_no_m", "opposite_no_m"]), on=["phone_no_m", "opposite_no_m"])
                      .join(passive_sms_user.set_index(["phone_no_m", "opposite_no_m"]), on=["phone_no_m", "opposite_no_m"]).fillna(0))
        result_sms["interactive_sms_user_cnt"] = result_sms.apply(lambda x: 1 if (x["initiative_sms_label"] == 1 and x["passive_sms_label"] == 1) else 0, axis=1)
        result_sms = result_sms[["phone_no_m", "interactive_sms_user_cnt"]].groupby(["phone_no_m"]).sum()

        result = (self.train_user[["phone_no_m", "label"]]
                  .join(voc_user_cnt, on=["phone_no_m"])
                  .join(result_voc, on=["phone_no_m"])
                  .join(sms_user_cnt, on=["phone_no_m"])
                  .join(result_sms, on=["phone_no_m"])
                  .fillna(0))
        result["interactive_call_user_ratio"] = result.apply(lambda x:x["interactive_call_user_cnt"]/x["call_user_cnt"] if x["call_user_cnt"]>0 else 0, axis=1)
        result["interactive_sms_user_ratio"] = result.apply(lambda x: x["interactive_sms_user_cnt"] / x["sms_user_cnt"] if x["sms_user_cnt"] > 0 else 0, axis=1)
        return result.drop(columns=["call_user_cnt", "sms_user_cnt"])

    # 拨打、接听电话和发送、接受短信的活跃天数差值
    def initiative_passive_activate_days_diff(self):
        # 通话相关
        tmp_data = self.train_voc[["phone_no_m", "start_datetime", "calltype_id"]].copy()
        tmp_data["date"] = tmp_data[["start_datetime"]].apply(lambda x: x["start_datetime"][0:10], axis=1)

        initiative_call_active_days = tmp_data[tmp_data["calltype_id"]==1][["phone_no_m", "date"]].drop_duplicates().groupby(["phone_no_m"]).count()
        initiative_call_active_days.columns = ["initiative_call_active_days"]

        passive_call_active_days = tmp_data[tmp_data["calltype_id"] == 2][["phone_no_m", "date"]].drop_duplicates().groupby(["phone_no_m"]).count()
        passive_call_active_days.columns = ["passive_call_active_days"]

        # 短信相关
        tmp_data = self.train_sms[["phone_no_m", "request_datetime", "calltype_id"]].copy()
        tmp_data["date"] = tmp_data[["request_datetime"]].apply(lambda x: x["request_datetime"][0:10], axis=1)
        initiative_sms_active_days = tmp_data[tmp_data["calltype_id"]==1][["phone_no_m", "date"]].drop_duplicates().groupby(["phone_no_m"]).count()
        initiative_sms_active_days.columns = ["initiative_sms_active_days"]

        passive_sms_active_days = tmp_data[tmp_data["calltype_id"] == 2][["phone_no_m", "date"]].drop_duplicates().groupby(["phone_no_m"]).count()
        passive_sms_active_days.columns = ["passive_sms_active_days"]

        # 数据融合
        result = (self.train_user[["phone_no_m", "label"]]
                  .join(initiative_call_active_days, on=["phone_no_m"])
                  .join(passive_call_active_days, on=["phone_no_m"])
                  .join(initiative_sms_active_days, on=["phone_no_m"])
                  .join(passive_sms_active_days, on=["phone_no_m"]).fillna(0))
        result["call_activate_days_diff"] = result.apply(lambda x: x["initiative_call_active_days"]-x["passive_call_active_days"], axis=1)
        result["sms_activate_days_diff"] = result.apply(lambda x: x["initiative_sms_active_days"] - x["passive_sms_active_days"], axis=1)
        return result

    # 相同时间与相同用户发送与接受短信的次数
    def multiple_sms_cnt(self):
        initial_temp_data = self.train_sms[self.train_sms["calltype_id"]==1].groupby(["phone_no_m", "opposite_no_m", "request_datetime"]).count().reset_index()
        passive_temp_data = self.train_sms[self.train_sms["calltype_id"]==2].groupby(["phone_no_m", "opposite_no_m", "request_datetime"]).count().reset_index()

        initial_temp_data["multiple_initial_sms_cnt"]=initial_temp_data.apply(lambda x: 1 if x["calltype_id"]>1 else 0, axis=1)
        passive_temp_data["multiple_passive_sms_cnt"]=passive_temp_data.apply(lambda x: 1 if x["calltype_id"]>1 else 0, axis=1)

        initial_data = initial_temp_data[["phone_no_m", "multiple_initial_sms_cnt"]].groupby("phone_no_m").sum()
        passive_data = passive_temp_data[["phone_no_m", "multiple_passive_sms_cnt"]].groupby("phone_no_m").sum()

        result = self.train_user[["phone_no_m", "label"]].join(initial_data, on=["phone_no_m"]).join(passive_data, on=["phone_no_m"]).fillna(0)

        return result

    # 通话时长相关
    def voc_dur_info(self):
        all_dur_info = self.train_voc[["phone_no_m", "call_dur"]].fillna(0).groupby("phone_no_m").sum()
        initial_dur_info = (self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "call_dur"]]
                            .fillna(0).groupby("phone_no_m").sum())
        initial_dur_info.columns=["initial_call_dur"]

        passive_dur_info = (self.train_voc[self.train_voc["calltype_id"] == 2][["phone_no_m", "call_dur"]]
                            .fillna(0).groupby("phone_no_m").sum())
        passive_dur_info.columns = ["passive_call_dur"]

        turn_dur_info = (self.train_voc[self.train_voc["calltype_id"] == 3][["phone_no_m", "call_dur"]]
                            .fillna(0).groupby("phone_no_m").sum())
        turn_dur_info.columns = ["turn_call_dur"]

        result = (self.train_user[["phone_no_m", "label"]]
                  .join(all_dur_info, on=["phone_no_m"])
                  .join(turn_dur_info, on=["phone_no_m"])
                  .join(initial_dur_info, on=["phone_no_m"])
                  .join(passive_dur_info, on=["phone_no_m"])
                  .fillna(0))
        result["passive_call_dur_ratio"] = (result[["passive_call_dur", "call_dur"]]
            .apply(lambda x: x["passive_call_dur"]/x["call_dur"] if x["call_dur"]>0 else 0, axis=1))
        result["initial_call_dur_ratio"] = (result[["initial_call_dur", "call_dur"]]
            .apply(lambda x: x["initial_call_dur"] / x["call_dur"] if x["call_dur"] > 0 else 0, axis=1))
        result["turn_call_dur_ratio"] = (result[["turn_call_dur", "call_dur"]]
            .apply(lambda x: x["turn_call_dur"] / x["call_dur"] if x["call_dur"] > 0 else 0, axis=1))

        active_days = self.active_days()
        result = result.join(active_days.drop(columns=["label"]).set_index("phone_no_m"), on=["phone_no_m"])

        result["passive_call_daily_dur"] = (result[["passive_call_dur", "active_days"]]
            .apply(lambda x: x["passive_call_dur"] / x["active_days"] if x["active_days"] > 0 else 0, axis=1))
        result["initial_call_daily_dur"] = (result[["initial_call_dur", "active_days"]]
            .apply(lambda x: x["initial_call_dur"] / x["active_days"] if x["active_days"] > 0 else 0, axis=1))
        result["turn_call_daily_dur"] = (result[["turn_call_dur", "active_days"]]
            .apply(lambda x: x["turn_call_dur"] / x["active_days"] if x["active_days"] > 0 else 0, axis=1))

        temp_data = self.train_voc[["phone_no_m", "calltype_id"]].copy()
        for i in range(1,4,1):
            temp_data["call_type_"+str(i)+"_cnt"] = temp_data[["calltype_id"]].apply(lambda x: 1 if x["calltype_id"]==i else 0, axis=1)
        temp_data = temp_data.drop(columns=["calltype_id"]).groupby(["phone_no_m"]).sum()
        temp_data = self.active_days().join(temp_data, on=["phone_no_m"]).fillna(0)
        for i in range(1,4):
            temp_data["daily_call_type_"+str(i)+"_cnt"] = (temp_data[["call_type_"+str(i)+"_cnt", "active_days"]]
                                                           .apply(lambda x: x["call_type_"+str(i)+"_cnt"]/x["active_days"] if x["active_days"]>0 else 0, axis=1))
        return (result.join(temp_data.drop(columns=["label", "active_days"]).set_index("phone_no_m"), on=["phone_no_m"])
                .fillna(0).drop(columns=["call_type_1_cnt", "call_type_2_cnt", "call_type_3_cnt"]))

    # 区域数量
    def county_cnt(self):
        initial_voc = (self.train_voc[self.train_voc["calltype_id"]==1]
                       .dropna(subset=["county_name"])[["phone_no_m", "county_name"]]
                       .drop_duplicates().groupby("phone_no_m").count())
        initial_voc.columns = ["initial_voc_county_cnt"]

        passive_voc = (self.train_voc[self.train_voc["calltype_id"]==2]
                       .dropna(subset=["county_name"])[["phone_no_m", "county_name"]]
                       .drop_duplicates().groupby("phone_no_m").count())
        passive_voc.columns = ["passive_voc_county"]

        turn_voc = (self.train_voc[self.train_voc["calltype_id"] == 3]
                       .dropna(subset=["county_name"])[["phone_no_m", "county_name"]]
                       .drop_duplicates().groupby("phone_no_m").count())
        turn_voc.columns = ["turn_voc_county"]

        return (self.train_user[["phone_no_m", "label"]]
                .join(initial_voc, on=["phone_no_m"])
                .join(passive_voc, on=["phone_no_m"])
                .join(turn_voc, on=["phone_no_m"])
                .fillna(0))

    def app_flow(self):
        data_filtered = self.train_app[self.train_app["month_id"]=="2020-03"][['phone_no_m', 'busi_name', 'flow']].copy()
        data_filtered["user_rank"] = [int(x) for x in data_filtered.groupby("phone_no_m")["flow"].rank(ascending=False)]
        first_flow_app = (data_filtered[data_filtered["user_rank"]==1]
            .reset_index().join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"])
                          [["phone_no_m", "busi_name", "label"]])

    def app_avg_open_cnt(self):
        app_open_cnt = self.train_app[["phone_no_m", "busi_name"]].groupby("phone_no_m").count()
        app_open_cnt.columns = ["app_open_cnt"]

        app_cnt = self.train_app[["phone_no_m", "busi_name"]].drop_duplicates().groupby("phone_no_m").count()
        app_cnt.columns = ["app_cnt"]

        final_data = (self.train_user[["phone_no_m", "label"]]
                      .join(app_open_cnt, on="phone_no_m").join(app_cnt, on="phone_no_m").fillna(0))
        final_data["app_avg_open_cnt"] = final_data["app_open_cnt"]/final_data["app_cnt"]
        print(final_data.corr()["label"])
        return final_data

    # 同天发送短信的间隔
    def sms_type_1_time_interval(self):
        tmp_data = self.train_sms[self.train_sms["calltype_id"] == 1][["phone_no_m", "request_datetime"]].copy()
        tmp_data["date"] = tmp_data.apply(lambda x: x["request_datetime"][0:10], axis=1)
        tmp_data["datetime"] = tmp_data.apply(lambda x: dt.datetime.strptime(x["request_datetime"], "%Y-%m-%d %H:%M:%S"), axis=1)
        tmp_data["timestamp"] = tmp_data.apply(lambda x: int(time.mktime(x["datetime"].timetuple())), axis=1)

        tmp_data["rank"] = [int(x) for x in tmp_data.groupby("phone_no_m")["timestamp"].rank(ascending=True)]
        tmp_data["next_rank"] = tmp_data.apply(lambda x: x["rank"] + 1, axis=1)

        tmp_data_next = tmp_data[["phone_no_m", "rank", "date", "datetime"]].copy()
        tmp_data_next.columns = ["phone_no_m", "rank", "date","next_datetime"]

        merge_data = tmp_data[["phone_no_m", "next_rank", "date", "datetime"]].join(
            tmp_data_next.set_index(["phone_no_m", "rank", "date"]), on=["phone_no_m", "next_rank", "date"])
        merge_data = merge_data.dropna(subset=["next_datetime"])

        merge_data["sms_interval"] = merge_data.apply(lambda x: (x["next_datetime"] - x["datetime"]).seconds, axis=1)

        final_result = merge_data[["phone_no_m", "sms_interval"]].groupby("phone_no_m").agg(
            [np.min, np.max, np.mean, np.median, np.std])
        final_result.columns = ["initiative_sms_interval_min", "initiative_sms_interval_max", "initiative_sms_interval_mean",
                            "initiative_sms_interval_median", "initiative_sms_interval_std"]
        final_result = self.train_user[["phone_no_m", "label"]].join(final_result, on=["phone_no_m"]).fillna(0)
        final_result.to_excel("sms_interval_check.xlsx")
        final_result[final_result["initiative_sms_interval_mean"]>0].corr()
        print(final_result.corr()["label"])
        return final_result

    # 根据时间段内发送短信的用户数，评定风险等级
    def avg_sms_type_1_user_per_interval_class(self):
        final_result = self.avg_sms_type_1_user_per_interval()
        final_result["avg_sms_type_1_user_per_interval_class"] = final_result.apply(lambda x: avg_sms_type_1_user_per_interval_class_define(x["sms_type_1_avg_user_per_interval"]), axis=1)
        return final_result[["phone_no_m", "avg_sms_type_1_user_per_interval_class"]].copy()


    # 单一时间段发送短信的不同用户数
    def avg_sms_type_1_user_per_interval(self):
        tmp_data = self.train_sms[self.train_sms["calltype_id"] == 1][["phone_no_m", "opposite_no_m", "request_datetime"]].copy()
        # 计算时间段，时间段为日期加上小时，格式为"yyyy-MM-dd HH"
        tmp_data["interval"] = tmp_data.apply(lambda x: x["request_datetime"][0:13], axis=1)

        tmp_sms_user = tmp_data[["phone_no_m", "opposite_no_m", "interval"]].drop_duplicates().groupby(["phone_no_m", "interval"]).count().reset_index()
        tmp_sms_user.columns=["phone_no_m", "interval", "sms_type_1_user"]

        final_result = tmp_sms_user[["phone_no_m", "sms_type_1_user"]].groupby(["phone_no_m"]).agg(
            [np.min, np.max, np.mean, np.median, np.std]).fillna(0)
        final_result.columns = ["sms_type_1_min_user_per_interval", "sms_type_1_max_user_per_interval",
                                "sms_type_1_avg_user_per_interval", "sms_type_1_median_user_per_interval",
                                "sms_type_1_std_user_per_interval"]
        final_result = self.train_user[["phone_no_m", "label"]].join(final_result, on=["phone_no_m"]).fillna(0)
        print(final_result.corr()["label"])
        return final_result


    # 单一时间段发送的短信数目
    def avg_sms_type_1_cnt_per_interval(self):
        tmp_data = self.train_sms[self.train_sms["calltype_id"] == 1][["phone_no_m", "opposite_no_m", "request_datetime"]].copy()

        # 计算时间段，时间段为日期加上小时，格式为"yyyy-MM-dd HH"
        tmp_data["interval"] = tmp_data.apply(lambda x: x["request_datetime"][0:13], axis=1)

        tmp_sms_cnt = tmp_data[["phone_no_m", "interval", "request_datetime"]].groupby(["phone_no_m", "interval"]).count().reset_index()
        tmp_sms_cnt.columns = ["phone_no_m", "interval", "sms_type_1_cnt"]

        final_result = tmp_sms_cnt[["phone_no_m", "sms_type_1_cnt"]].groupby(["phone_no_m"]).agg([np.min, np.max, np.mean, np.median, np.std]).fillna(0)
        final_result.columns = ["sms_type_1_min_cnt_per_interval", "sms_type_1_max_cnt_per_interval", "sms_type_1_avg_cnt_per_interval"
                                ,"sms_type_1_median_cnt_per_interval", "sms_type_1_std_cnt_per_interval"]
        final_result = self.train_user[["phone_no_m", "label"]].join(final_result, on=["phone_no_m"]).fillna(0)
        print(final_result.corr()["label"])
        return final_result


    # 给每个用户发送的平均短信数
    def avg_sms_type_1_cnt_per_user(self):
        tmp_sms_cnt = self.train_sms[self.train_sms["calltype_id"]==1][["phone_no_m", "opposite_no_m"]].groupby("phone_no_m").count()
        tmp_sms_cnt.columns = ["sms_type_1_cnt"]

        tmp_sms_user = self.train_sms[self.train_sms["calltype_id"]==1][["phone_no_m", "opposite_no_m"]].drop_duplicates().groupby("phone_no_m").count()
        tmp_sms_user.columns = ["sms_type_1_user"]

        final_result = (self.train_user[["phone_no_m", "label"]]
                        .join(tmp_sms_cnt, on=["phone_no_m"])
                        .join(tmp_sms_user, on=["phone_no_m"])
                        .fillna(0))
        final_result["sms_type_1_cnt_per_user"] = final_result.apply(lambda x: x["sms_type_1_cnt"]/x["sms_type_1_user"] if x["sms_type_1_user"]>0 else 0, axis=1)


    # 计算各用户的被动通话记录之间的通话间隔
    def passive_call_interval_cnt(self):
        final_result = calculate_interval(self.train_voc[self.train_voc["calltype_id"]==2][["phone_no_m", "start_datetime", "call_dur"]],
                           self.train_user[["phone_no_m", "label"]],
                          ["passive_call_interval_min", "passive_call_interval_max", "passive_call_interval_mean",
                           "passive_call_interval_median", "passive_call_interval_std"])
        print(final_result.corr()["label"])
        return final_result

    # 计算各用户的主动通话记录之间的通话间隔
    def initiative_call_interval_cnt(self):
        final_result = calculate_interval(self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "start_datetime", "call_dur"]],
                           self.train_user[["phone_no_m", "label"]],
                           ["initiative_call_interval_min", "initiative_call_interval_max", "initiative_call_interval_mean",
                            "initiative_call_interval_median", "initiative_call_interval_std"])
        return final_result


    # 计算各用户的通话记录之间的通话间隔
    def call_interval_cnt(self):
        final_result = calculate_interval(
            self.train_voc[["phone_no_m", "start_datetime", "call_dur"]],
            self.train_user[["phone_no_m", "label"]],
            ["call_interval_min", "call_interval_max", "call_interval_mean", "call_interval_median", "call_interval_std"]
        )
        return final_result

    # 短时间通话占比
    def call_dur_analysis(self):
        call_cnt = self.train_voc[ self.train_voc["calltype_id"]==1][["phone_no_m", "call_dur"]].groupby(["phone_no_m"]).count()
        call_cnt.columns = ["call_cnt"]

        short_call_cnt = self.train_voc[(self.train_voc["calltype_id"] == 1) & (self.train_voc["call_dur"] <= 10)][["phone_no_m", "call_dur"]].groupby(["phone_no_m"]).count()
        short_call_cnt.columns = ["short_call_cnt"]

        data = self.train_user[["phone_no_m", "label"]].join(call_cnt, on=["phone_no_m"]).join(short_call_cnt, on=["phone_no_m"])
        data["short_call_ratio"] = data.apply(lambda x: x["short_call_cnt"]/x["call_cnt"] if x["call_cnt"]>0 else 0, axis=1)
        data = data.fillna(0)

        find_short_call_dur(self.train_voc, self.train_user, 1)

        result = pd.DataFrame(columns=["threshold_dur", "call_cnt", "short_call_cnt", "short_call_ratio"])
        for i in range(60):
            current_result = find_short_call_dur(self.train_voc, self.train_user, i)
            result = result.append(
                pd.DataFrame({
                    "threshold_dur": [i],
                    "call_cnt": [current_result[1]],
                    "short_call_cnt": [current_result[2]],
                    "short_call_ratio": [current_result[3]]
                })
            )

    def call_city_cnt(self):
        tmp_data = self.train_voc[ self.train_voc["calltype_id"]==1][["phone_no_m", "city_name"]].drop_duplicates().groupby(["phone_no_m"]).count()
        tmp_data.columns = ["city_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"]).fillna(0)
        return tmp_data


    # 用户活跃天数
    def active_days(self):
        tmp_data = self.train_voc[["phone_no_m", "start_datetime"]].copy()
        tmp_data["date"] = tmp_data.apply(lambda x: x["start_datetime"][0:10], axis=1)
        tmp_data = tmp_data[["phone_no_m", "date"]].drop_duplicates().groupby(by=["phone_no_m"]).count()
        tmp_data.columns=["active_days"]
        tmp_data = self.train_user[["phone_no_m","label"]].join(tmp_data, on=["phone_no_m"]).fillna(0)
        return tmp_data

    # 礼拜中的各天主呼次数情况
    def week_day_statistic(self):
        tmp_data = self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "start_datetime"]].copy()
        tmp_data["datetime"] = tmp_data.apply(lambda x: dt.datetime.strptime(x["start_datetime"], "%Y-%m-%d %H:%M:%S"), axis=1)
        tmp_data["weekday"] = tmp_data.apply(lambda x: x["datetime"].weekday()+1, axis=1)

        for i in range(1,8):
            tmp_data["weekday_"+str(i)] = tmp_data.apply(lambda x: 1 if x["weekday"]==i else 0, axis=1)

        tmp_data = tmp_data[["phone_no_m", "weekday_1", "weekday_2", "weekday_3", "weekday_4", "weekday_5", "weekday_6", "weekday_7"]].groupby(["phone_no_m"]).sum()
        tmp_data["voc_cnt"] = tmp_data.apply(lambda x: x["weekday_1"]+x["weekday_2"]+x["weekday_3"]+x["weekday_4"]
                                                       + x["weekday_5"]+x["weekday_6"]+x["weekday_7"], axis=1)
        for i in range(1, 8):
            tmp_data["weekday_"+str(i)+"_ratio"] = tmp_data.apply(lambda x: x["weekday_"+str(i)]/x["voc_cnt"] if x["voc_cnt"]>0 else 0, axis=1)
        return tmp_data


    def get_white_black_app_cnt(self):
        tmp_data = self.train_app[['phone_no_m', 'busi_name']].drop_duplicates().copy()
        apps = pd.read_excel("Apps/app黑白用户占比统计.xlsx", sheet_name=0, header=0)
        black_app = apps[apps["欺诈用户占比"]>=0.6]["APP"].values
        white_app = apps[apps["欺诈用户占比"] == 0]["APP"].values

        tmp_data["black_app_cnt"] = tmp_data.apply(lambda x: 1 if x["busi_name"] in black_app else 0, axis=1)
        tmp_data["white_app_cnt"] = tmp_data.apply(lambda x: 1 if x["busi_name"] in white_app else 0, axis=1)

        tmp_data = tmp_data[['phone_no_m', 'black_app_cnt', 'white_app_cnt']].groupby(["phone_no_m"]).sum()
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"])
        tmp_data = tmp_data.fillna(0)
        return tmp_data


    # 每六个小时拨打电话用户数
    def six_hour_voc_user(self):
        tmp_data = self.train_voc[self.train_voc["calltype_id"] == 1][["phone_no_m", "start_datetime", "opposite_no_m"]].copy()
        tmp_data["hour"] = tmp_data.apply(lambda x: int(x[1][11:13]), axis=1)
        tmp_data["interval"] = tmp_data.apply(lambda x: int(x['hour'] / 6), axis=1)
        tmp_data["day"] = tmp_data.apply(lambda x: x[1][0:10], axis=1)
        tmp_data["time"] = tmp_data.apply(lambda x: str(x["day"]) + "-" + str(x["interval"]), axis=1)

        tmp_data = tmp_data[["phone_no_m", "opposite_no_m", "time"]].drop_duplicates()
        tmp_data["user_cnt"] = [1]*len(tmp_data)

        tmp_data = tmp_data.groupby(by=["phone_no_m", "time"]).count()
        tmp_data = tmp_data.reset_index()

        tmp_data = tmp_data.groupby(["phone_no_m"]).agg([np.max, np.mean, np.median, np.std])
        tmp_data = tmp_data.reset_index()
        tmp_data.columns = ["phone_no_m", "voc_6_cnt_max", "voc_6_cnt_mean", "voc_6_cnt_median", "voc_6_cnt_std"]

        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data.set_index("phone_no_m"),
                                                                 on=["phone_no_m"]).fillna(0)
        return tmp_data

    # 每六个小时拨打电话次数
    def six_hour_voc_cnt(self):
        tmp_data = self.train_voc[self.train_voc["calltype_id"] == 1][["phone_no_m", "start_datetime"]].copy()
        tmp_data["hour"] = tmp_data.apply(lambda x: int(x[1][11:13]), axis=1)
        tmp_data["interval"] = tmp_data.apply(lambda x: int(x['hour']/6), axis=1)
        tmp_data["day"] = tmp_data.apply(lambda x: x[1][0:10], axis=1)
        tmp_data["time"] = tmp_data.apply(lambda x: str(x["day"])+"-"+str(x["interval"]), axis=1)
        tmp_data = tmp_data[["phone_no_m", "time", "start_datetime"]].groupby(by=["phone_no_m", "time"]).count()
        tmp_data = tmp_data.reset_index()

        tmp_data = tmp_data.groupby(["phone_no_m"]).agg([np.max, np.mean, np.median, np.std])
        tmp_data = tmp_data.reset_index()
        tmp_data.columns = ["phone_no_m", "voc_6_cnt_max", "voc_6_cnt_mean", "voc_6_cnt_median", "voc_6_cnt_std"]

        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"]).fillna(0)
        return tmp_data

    # 通话记录中imei的个数
    def voc_imei_cnt(self):
        tmp_data = self.train_voc[["phone_no_m", "imei_m"]].drop_duplicates().copy()
        tmp_data = tmp_data.groupby(["phone_no_m"]).count()
        tmp_data.columns = ["imei_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"]).fillna(0)
        return tmp_data


    # app数量与标签之前的关系
    def flow_cnt(self):
        tmp_data = self.train_app[["phone_no_m", "flow"]].copy()
        tmp_data = tmp_data.dropna(subset=["phone_no_m"])
        tmp_data = tmp_data.groupby(["phone_no_m"]).sum()
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"]).fillna(0)
        return tmp_data

    # app数量与标签之前的关系
    def app_cnt(self):
        tmp_data = self.train_app[["phone_no_m", "busi_name"]].drop_duplicates().copy()
        tmp_data = tmp_data.dropna(subset=["busi_name"])
        tmp_data = tmp_data.groupby(["phone_no_m"]).count()
        tmp_data.columns = ["app_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"]).fillna(0)
        return tmp_data

    # 高危app列表
    def app_app_name(self):
        tmp_data = self.train_app.dropna(subset=["busi_name"]).copy()
        tmp_data = tmp_data.dropna(subset=["phone_no_m"])
        tmp_data = tmp_data[["phone_no_m", "busi_name"]].drop_duplicates().join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on="phone_no_m")
        tmp_data["user_cnt"] = tmp_data.apply(lambda x: 1, axis=1)
        tmp_data = tmp_data.dropna(subset=["label"])
        tmp_data["fake_cnt"] = tmp_data.apply(lambda x: 1 if x["label"] == 1 else 0, axis=1)

        tmp_data[["busi_name", "user_cnt", "fake_cnt"]].groupby(["busi_name"]).sum()
        tmp_data = tmp_data[["busi_name", "user_cnt", "fake_cnt"]].groupby(["busi_name"]).sum()
        tmp_data = tmp_data.reset_index()

        tmp_data["fake_ratio"] = tmp_data.apply(lambda x: x["fake_cnt"]/x["user_cnt"] if x["user_cnt"]>0 else 0, axis=1)

        high_risk_app = tmp_data[tmp_data["fake_ratio"] >= 0.6]["busi_name"].values

        return tmp_data[tmp_data["fake_ratio"]>=0.8]["busi_name"].values

    # 各时段短信次数及占比
    def get_sms_time_interval_ratio(self):
        tmp_data = self.train_sms[["phone_no_m", "request_datetime"]].copy()
        tmp_data["hour"] = tmp_data.apply(lambda x: int(x[1][14:16]), axis=1)
        tmp_data = tmp_data.groupby(["phone_no_m", "hour"]).count()
        tmp_data = pd.DataFrame({
            "phone_no_m": [x[0] for x in tmp_data.index],
            "hour": [x[1] for x in tmp_data.index],
            "voc_cnt": tmp_data["request_datetime"].values
        })

        for i in range(24):
            tmp_data["interval_"+str(i)+"_cnt"] = tmp_data.apply(lambda x: x[2] if x[1] == i else 0, axis=1)

        tmp_data = tmp_data.groupby(["phone_no_m"]).sum()

        for i in range(24):
            tmp_data["interval_"+str(i)+"_ratio"] = tmp_data.apply(lambda x: x["interval_"+str(i)+"_cnt"] / x["voc_cnt"], axis=1)

        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 短信发送次数
    def get_sms_cnt(self):
        tmp_data = self.train_sms[["phone_no_m", "request_datetime"]].groupby(["phone_no_m"]).count()
        tmp_data.columns = ["sms_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"])
        tmp_data_2 = self.train_sms[["phone_no_m", "calltype_id"]].copy()
        tmp_data_2["call_type_1_cnt"] = tmp_data_2.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
        tmp_data_2["call_type_2_cnt"] = tmp_data_2.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
        tmp_data_2["call_cnt"] = tmp_data_2.apply(lambda x: x["call_type_1_cnt"] + x["call_type_2_cnt"], axis=1)

        tmp_data_2 = tmp_data_2.groupby(["phone_no_m"]).sum()

        tmp_data_2["call_type_1_ratio"] = tmp_data_2.apply(
            lambda x: x["call_type_1_cnt"] / x["call_cnt"] if x["call_cnt"] > 0 else 0, axis=1)
        tmp_data_2["call_type_2_ratio"] = tmp_data_2.apply(
            lambda x: x["call_type_2_cnt"] / x["call_cnt"] if x["call_cnt"] > 0 else 0, axis=1)
        tmp_data = tmp_data.join(tmp_data_2, on=["phone_no_m"])
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 主呼被呼占比统计
    def get_voc_call_type_id(self):
        tmp_data = self.train_voc[["phone_no_m", "calltype_id"]].copy()
        tmp_data["call_type_1_cnt"] = tmp_data.apply(lambda x: 1 if x["calltype_id"] == 1 else 0, axis=1)
        tmp_data["call_type_2_cnt"] = tmp_data.apply(lambda x: 1 if x["calltype_id"] == 2 else 0, axis=1)
        tmp_data["call_type_3_cnt"] = tmp_data.apply(lambda x: 1 if x["calltype_id"] == 3 else 0, axis=1)
        tmp_data = tmp_data.groupby(["phone_no_m"]).sum()
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on=["phone_no_m"])
        tmp_data = tmp_data.fillna(0)
        tmp_data["call_cnt"] = tmp_data.apply(lambda x: x["call_type_1_cnt"]+x["call_type_2_cnt"]+x["call_type_3_cnt"], axis=1)
        tmp_data["call_type_1_ratio"] = tmp_data.apply(lambda x: x["call_type_1_cnt"]/x["call_cnt"] if x["call_cnt"]>0 else 0, axis=1)
        tmp_data["call_type_2_ratio"] = tmp_data.apply(
            lambda x: x["call_type_2_cnt"] / x["call_cnt"] if x["call_cnt"] > 0 else 0, axis=1)
        tmp_data["call_type_3_ratio"] = tmp_data.apply(
            lambda x: x["call_type_3_cnt"] / x["call_cnt"] if x["call_cnt"] > 0 else 0, axis=1)
        return tmp_data

    def get_test_user(self):
        data = pd.read_csv(os.path.join(self.TEST_DATA_DIR, "test_user.csv"), header=0)
        data["label"] = [0]*len(data)
        return data

    def get_test_voc(self):
        return pd.read_csv(os.path.join(self.TEST_DATA_DIR, "test_voc.csv"), header=0)

    def get_test_sms(self):
        return pd.read_csv(os.path.join(self.TEST_DATA_DIR, "test_sms.csv"), header=0)

    def get_test_app(self):
        return pd.read_csv(os.path.join(self.TEST_DATA_DIR, "test_app.csv"), header=0)

    def get_rematch_user(self):
        data = pd.read_csv(os.path.join(self.REMATCH_DATA_DIR, "test_user.csv"), header=0)
        data["label"] = [0]*len(data)
        return data

    def get_rematch_voc(self):
        return pd.read_csv(os.path.join(self.REMATCH_DATA_DIR, "test_voc.csv"), header=0)

    def get_rematch_sms(self):
        return pd.read_csv(os.path.join(self.REMATCH_DATA_DIR, "test_sms.csv"), header=0)

    def get_rematch_app(self):
        return pd.read_csv(os.path.join(self.REMATCH_DATA_DIR, "test_app.csv"), header=0)

    def get_train_user(self):
        # return pd.read_csv(os.path.join(self.TRAIN_DATA_DIR, "train_user.csv"), header=0)
        return pd.read_excel(os.path.join(self.FILTRATION_TRAIN_DATA_DIR, "filtration_train_user.xlsx"), header=0)

    def get_train_voc(self):
        # return pd.read_csv(os.path.join(self.TRAIN_DATA_DIR, "train_voc.csv"), header=0)
        return pd.read_excel(os.path.join(self.FILTRATION_TRAIN_DATA_DIR, "filtration_train_voc.xlsx"), header=0)

    def get_train_sms(self):
        # return pd.read_csv(os.path.join(self.TRAIN_DATA_DIR, "train_sms.csv"), header=0)
        return pd.read_excel(os.path.join(self.FILTRATION_TRAIN_DATA_DIR, "filtration_train_sms.xlsx"), header=0)

    def get_train_app(self):
        # return pd.read_csv(os.path.join(self.TRAIN_DATA_DIR, "train_app.csv"), header=0)
        return pd.read_excel(os.path.join(self.FILTRATION_TRAIN_DATA_DIR, "filtration_train_app.xlsx"), header=0)

    # 获取每个人的通话记录数
    def get_voc_cnt(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m"]].groupby(["phone_no_m"]).count()
        tmp_data.columns=["voc_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 获取每个人通话记录中的通话人数
    def get_voc_opposite_user_cnt(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m"]].drop_duplicates().groupby(["phone_no_m"]).count()
        tmp_data.columns = ["voc_user_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 通话记录与同一个人通话的最大最小次数、中位数、平均数、方差
    def get_voc_user_max_min_cnt(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m", "calltype_id"]].groupby(["phone_no_m", "opposite_no_m"]).count()
        phone_no_m = [x[0] for x in tmp_data.index]
        tmp_data = pd.DataFrame({
            "phone_no_m": phone_no_m,
            "voc_user_cnt": tmp_data["calltype_id"].values
        })
        tmp_data_agg = tmp_data.groupby(["phone_no_m"]).agg([np.min, np.max, np.mean, np.median, np.std])
        tmp_data_agg.columns = ["voc_user_max_cnt", "voc_user_min_cnt", "voc_user_mean_cnt", "voc_user_median_cnt",
                                "voc_user_std_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data_agg, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 判断用户一天与不同用户数进行通话的最大最小人数
    def get_voc_user_inner_day(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m", "start_datetime"]].copy()
        tmp_data["start_date"] = tmp_data[["start_datetime"]].apply(lambda x: x[0][0:10], axis=1)
        # 按照拨打用户 - 接听用户 - 日期进行去重
        tmp_data = tmp_data[["phone_no_m", "opposite_no_m", "start_date"]].drop_duplicates().copy()
        # 统计用户每天拨打的用户数
        tmp_data = tmp_data.groupby(["phone_no_m", "start_date"]).count()
        tmp_data = pd.DataFrame({
            "phone_no_m": [x[0] for x in tmp_data.index],
            "date": [x[1] for x in tmp_data.index],
            "user_cnt": tmp_data["opposite_no_m"].values
        })
        # 寻找用户每天拨打用户数的最大值最小值
        tmp_data = tmp_data[["phone_no_m", "user_cnt"]].groupby(["phone_no_m"]).agg([np.max, np.min])
        tmp_data.columns = ["user_max_cnt_inner_day", "user_min_cnt_inner_day"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 判断用户一天进行通话的最大最小次数
    def get_voc_cnt_inner_day(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m", "start_datetime"]].copy()
        tmp_data["start_date"] = tmp_data[["start_datetime"]].apply(lambda x: x[0][0:10], axis=1)
        # 统计用户每天拨打的拨打次数
        tmp_data = tmp_data.groupby(["phone_no_m", "start_date"]).count()
        tmp_data = pd.DataFrame({
            "phone_no_m": [x[0] for x in tmp_data.index],
            "date": [x[1] for x in tmp_data.index],
            "cnt": tmp_data["opposite_no_m"].values
        })
        # 寻找用户每天拨打用户数的最大值最小值
        tmp_data = tmp_data[["phone_no_m", "cnt"]].groupby(["phone_no_m"]).agg([np.max, np.min])
        tmp_data.columns = ["max_cnt_inner_day", "min_cnt_inner_day"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 获取通话时长的最大、最小、中位数、平均数、方差
    def get_voc_duration_indicator(self):
        tmp_data = self.train_voc[["phone_no_m", "call_dur"]].copy()
        tmp_data = tmp_data.groupby(["phone_no_m"]).agg([np.max, np.min, np.median, np.mean, np.std])
        tmp_data.columns = ["dur_max", "dur_min", "dur_median", "dur_mean", "dur_std"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data=tmp_data.fillna(0)
        return tmp_data

    # 各时段主动通话次数及占比
    def get_initiative_voc_time_interval_ratio(self):
        tmp_data = self.train_voc[self.train_voc["calltype_id"]==1][["phone_no_m", "start_datetime"]].copy()
        tmp_data["hour"] = tmp_data.apply(lambda x: int(x[1][11:13]), axis=1)
        tmp_data = tmp_data.groupby(["phone_no_m", "hour"]).count()
        tmp_data = pd.DataFrame({
            "phone_no_m": [x[0] for x in tmp_data.index],
            "hour": [x[1] for x in tmp_data.index],
            "voc_cnt": tmp_data["start_datetime"].values
        })

        for i in range(24):
            tmp_data["interval_"+str(i)+"_cnt"] = tmp_data.apply(lambda x: x[2] if x[1] == i else 0, axis=1)

        tmp_data = tmp_data.groupby(["phone_no_m"]).sum()

        for i in range(24):
            tmp_data["interval_"+str(i)+"_ratio"] = tmp_data.apply(lambda x: x["interval_"+str(i)+"_cnt"] / x["voc_cnt"], axis=1)

        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data


    # 各时段通话次数及占比
    def get_voc_time_interval_ratio(self):
        tmp_data = self.train_voc[["phone_no_m", "start_datetime"]].copy()
        tmp_data["hour"] = tmp_data.apply(lambda x: int(x[1][14:16]), axis=1)
        tmp_data = tmp_data.groupby(["phone_no_m", "hour"]).count()
        tmp_data = pd.DataFrame({
            "phone_no_m": [x[0] for x in tmp_data.index],
            "hour": [x[1] for x in tmp_data.index],
            "voc_cnt": tmp_data["start_datetime"].values
        })
        for i in range(24):
            tmp_data["interval_"+str(i)+"_cnt"] = tmp_data.apply(lambda x: x[2] if x[1] == i else 0, axis=1)

        tmp_data = tmp_data.groupby(["phone_no_m"]).sum()

        for i in range(24):
            tmp_data["interval_"+str(i)+"_ratio"] = tmp_data.apply(lambda x: x["interval_"+str(i)+"_cnt"] / x["voc_cnt"], axis=1)

        tmp_data = self.train_user[["phone_no_m", "label"]].join(tmp_data, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        return tmp_data

    # 与同一用户拨打的平均次数
    def get_user_avg_voc_cnt(self):
        tmp_data = self.train_voc[["phone_no_m", "opposite_no_m"]].copy()
        voc_cnt = tmp_data.groupby(["phone_no_m"]).count()
        voc_cnt.columns=["voc_cnt"]
        user_cnt = tmp_data.drop_duplicates().groupby(["phone_no_m"]).count()
        user_cnt.columns = ["user_cnt"]
        tmp_data = self.train_user[["phone_no_m", "label"]].join(voc_cnt, on="phone_no_m").join(user_cnt, on="phone_no_m")
        tmp_data = tmp_data.fillna(0)
        tmp_data["voc_cnt_per_user"]=tmp_data.apply(lambda x: x["voc_cnt"] / x["user_cnt"] if x["user_cnt"]>0 else 0, axis=1)
        return tmp_data

    # 寻找高危地区列表
    def search_high_risk_city_areas(self):
        tmp_data=self.train_user[["phone_no_m", "label"]].join(self.train_voc[["phone_no_m", "city_name"]].set_index("phone_no_m"), on="phone_no_m")
        tmp_data = tmp_data.drop_duplicates()
        # 删除城市名为空的数据
        tmp_data = tmp_data.dropna(subset=["city_name"])
        tmp_data["label_count"] = [1]*len(tmp_data)
        tmp_data = tmp_data.drop_duplicates()
        tmp_data = tmp_data.groupby(["city_name"]).sum()
        tmp_data["city_name"] = tmp_data.index
        tmp_data["bad_ratio"] = tmp_data.apply(lambda x: x["label"] / x["label_count"], axis=1)
        tmp_data = tmp_data.sort_values(by=["bad_ratio"], ascending=False)
        return tmp_data

    # 寻找高位地区列表（区县）
    def search_high_risk_county_areas(self):
        tmp_data=self.train_user[["phone_no_m", "label"]].join(self.train_voc[["phone_no_m", "county_name"]].set_index("phone_no_m"), on="phone_no_m")
        tmp_data = tmp_data.drop_duplicates()
        # 删除城市名为空的数据
        tmp_data = tmp_data.dropna(subset=["county_name"])
        tmp_data["label_count"] = [1]*len(tmp_data)
        tmp_data = tmp_data.drop_duplicates()
        tmp_data = tmp_data.groupby(["county_name"]).sum()
        tmp_data["bad_ratio"] = tmp_data.apply(lambda x: x["label"] / x["label_count"], axis=1)
        tmp_data = tmp_data.sort_values(by=["bad_ratio"], ascending=False)
        tmp_data.to_excel(r"C:\Users\Hao\PycharmProjects\match\match-telephone_fraud\high_risk_area_county.xlsx",
                          index=None)
        return tmp_data


def test_data_check():
    test_voc = self.train_voc[['phone_no_m', 'opposite_no_m']].groupby("phone_no_m").count()
    test_voc.columns = ["voc_cnt"]
    test_sms = self.train_sms[['phone_no_m', 'opposite_no_m']].groupby("phone_no_m").count()
    test_sms.columns = ["sms_cnt"]
    test_app = self.train_app[['phone_no_m', 'busi_name']].groupby("phone_no_m").count()
    test_app.columns = ["app_cnt"]

    final_merge = (self.train_user[["phone_no_m", "label"]]
                   .join(test_voc, on=["phone_no_m"])
                   .join(test_sms, on=["phone_no_m"])
                   .join(test_app, on=["phone_no_m"]).fillna(0))
    final_merge["cnt"] = final_merge.apply(lambda x: x["voc_cnt"]+x["sms_cnt"]+x["app_cnt"], axis=1)
    final_merge.to_excel("test_data_check.xlsx", index=None)

if __name__ == '__main__':
    self = Config()
    self.load_data()

    data = self.get_voc_opposite_user_cnt()

    tmp_data = self.get_voc_user_max_min_cnt()[["phone_no_m", "voc_user_min_cnt", "voc_user_mean_cnt", "voc_user_std_cnt"]]
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.get_voc_user_inner_day()[["phone_no_m", "user_max_cnt_inner_day", "user_min_cnt_inner_day"]].copy()
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.get_voc_cnt_inner_day()[["phone_no_m", "max_cnt_inner_day", "min_cnt_inner_day"]].copy()
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.get_user_avg_voc_cnt()[["phone_no_m", "voc_cnt_per_user"]].copy()
    data = data.join(tmp_data[["phone_no_m", "voc_cnt_per_user"]].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.get_voc_call_type_id()[["phone_no_m", "call_type_1_ratio", "call_type_2_ratio"]].copy()
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])

    data = data.join(self.train_user[["phone_no_m", "idcard_cnt"]].set_index("phone_no_m"), on=["phone_no_m"])

    data.to_excel(r"test_data.xlsx", index=None)

    tmp_data = self.get_sms_cnt()
    tmp_data=tmp_data[["phone_no_m", "call_type_1_ratio", "call_type_2_ratio", "sms_cnt"]]
    tmp_data.columns=["phone_no_m", "sms_type_1_ratio", "sms_type_2_ratio", "sms_cnt"]
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.app_cnt()
    data = data.join(tmp_data[["phone_no_m", "app_cnt"]].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.flow_cnt()
    data = data.join(tmp_data[["phone_no_m", "flow"]].set_index("phone_no_m"), on=["phone_no_m"])

    high_risk_app = pd.read_excel(r"high_risk_app.xlsx", header=0)
    high_risk_app = high_risk_app[high_risk_app["fake_ratio"]>=0.8][["busi_name", "fake_ratio"]].drop_duplicates().copy()

    tmp_data = self.train_app[["phone_no_m", "busi_name"]].join(high_risk_app.set_index("busi_name"), on=["busi_name"])
    tmp_data = tmp_data.dropna(subset=["fake_ratio"]).groupby(["phone_no_m"]).max()
    data = data.join(tmp_data[["fake_ratio"]], on=["phone_no_m"])
    data = data.fillna(0)
    data["fake_ratio"] = data.apply(lambda x: 1 if x["fake_ratio"]>0 else 0, axis=1)

    tmp_data = self.train_app.copy()
    tmp_data["is_high_risk_app"] = tmp_data.apply(lambda x: 1 if x["busi_name"] in high_risk_app else 0, axis=1)
    tmp_data = tmp_data[["phone_no_m", "is_high_risk_app"]].groupby(["phone_no_m"]).max().reset_index()
    data = data.join(tmp_data.set_index("phone_no_m"), on=["phone_no_m"])
    data["fake_ratio"] = data.apply(lambda x: x["is_high_risk_app"], axis=1)
    data = data[
        ['phone_no_m', 'label', 'voc_user_cnt', 'voc_user_min_cnt',
         'voc_user_mean_cnt', 'voc_user_std_cnt', 'user_max_cnt_inner_day',
         'user_min_cnt_inner_day', 'max_cnt_inner_day', 'min_cnt_inner_day',
         'voc_cnt_per_user', 'call_type_1_ratio', 'call_type_2_ratio',
         'idcard_cnt', 'sms_type_1_ratio', 'sms_type_2_ratio', 'sms_cnt',
         'app_cnt', 'flow', 'fake_ratio', 'voc_6_user_mean', 'voc_6_cnt_mean',
         'imei_cnt', 'interval_6_ratio', 'interval_7_ratio', 'interval_14_ratio',
         'interval_15_ratio', 'interval_16_ratio'
         ]]

    tmp_data = self.get_white_black_app_cnt()
    data = data.join(tmp_data[['phone_no_m', 'black_app_cnt', 'white_app_cnt']].set_index("phone_no_m"),
                     on=["phone_no_m"])

    data["black_app_ratio"] = data.apply(lambda x: x["black_app_cnt"] / x["app_cnt"] if x["app_cnt"] > 0 else 0, axis=1)
    data["white_app_ratio"] = data.apply(lambda x: x["white_app_cnt"] / x["app_cnt"] if x["app_cnt"] > 0 else 0, axis=1)

    tmp_data = self.active_days()
    data = data.join(tmp_data[['phone_no_m', 'active_days']].set_index("phone_no_m"),
                     on=["phone_no_m"])

    # 20200630添加
    tmp_data = self.call_city_cnt()
    data = data.join(tmp_data[['phone_no_m', 'city_cnt']].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.call_interval_cnt()
    data = data.join(tmp_data[['phone_no_m', 'call_interval_mean']].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.initiative_call_interval_cnt()
    data = data.join(tmp_data[['phone_no_m', 'initiative_call_interval_mean']].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.avg_sms_type_1_cnt_per_interval()
    data = data.join(tmp_data[['phone_no_m', 'sms_type_1_avg_cnt_per_interval']].set_index("phone_no_m"), on=["phone_no_m"])

    tmp_data = self.avg_sms_type_1_user_per_interval_class()
    data = data.join(tmp_data[['phone_no_m', 'avg_sms_type_1_user_per_interval_class']].set_index("phone_no_m"), on=["phone_no_m"])

    # 20200701添加
    tmp_data = self.app_avg_open_cnt()
    data = data.join(tmp_data[['phone_no_m', 'app_avg_open_cnt']].set_index("phone_no_m"), on=["phone_no_m"])

    data.to_excel(r"train_data.xlsx", index=None)
    data.to_excel(r"test_data.xlsx", index=None)
    data = pd.read_excel(r"train_data.xlsx", header=0)
    data = pd.read_excel(r"test_data.xlsx", header=0)


