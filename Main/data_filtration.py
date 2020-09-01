# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/2 9:44
# IDE：PyCharm

from Main import *

if __name__ == '__main__':
    self = Config()

    # 筛选2020年3月份的通话记录
    self.train_voc["month_id"] = self.train_voc[["start_datetime"]].apply(lambda x: x["start_datetime"][0:7], axis = 1)
    data_filtered = self.train_voc[self.train_voc["month_id"] == "2020-03"].drop(columns=["month_id"])
    data_filtered.to_excel("filtration_train_voc.xlsx", index=None)

    # 筛选2020年3月份的短信记录
    self.train_sms["month_id"] = self.train_sms[["request_datetime"]].apply(lambda x: x["request_datetime"][0:7], axis=1)
    data_filtered = self.train_sms[self.train_sms["month_id"] == "2020-03"].drop(columns=["month_id"])
    data_filtered.to_excel("filtration_train_sms.xlsx", index=None)

    # 筛选2020年3月份的app流量记录
    data_filtered = self.train_app[self.train_app["month_id"] == "2020-03"]
    data_filtered.to_excel("filtration_train_app.xlsx", index=None)

    self.train_user.to_excel("filtration_train_user.xlsx", index=None)