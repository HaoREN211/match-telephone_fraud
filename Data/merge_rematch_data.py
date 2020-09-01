# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/23 9:48
# IDE：PyCharm

import pandas as pd
import os

FIRST_MATCH_RESULT = "初赛结果.csv"

# 初赛的训练集
FIRST_MATCH_TRAIN_USER = "Data/filtration_train/filtration_train_user.xlsx"
FIRST_MATCH_TRAIN_APP = "Data/filtration_train/filtration_train_app.xlsx"
FIRST_MATCH_TRAIN_SMS = "Data/filtration_train/filtration_train_sms.xlsx"
FIRST_MATCH_TRAIN_VOC = "Data/filtration_train/filtration_train_voc.xlsx"

# 初赛的目标数据
FIRST_MATCH_TEST_USER = "Data/test/test_user.csv"
FIRST_MATCH_TEST_APP = "Data/test/test_app.csv"
FIRST_MATCH_TEST_SMS = "Data/test/test_sms.csv"
FIRST_MATCH_TEST_VOC = "Data/test/test_voc.csv"

# 合并用户数据
def merge_user_data():
    fir_match_result = pd.read_csv(FIRST_MATCH_RESULT, header=0)
    train_user = pd.read_excel(FIRST_MATCH_TRAIN_USER)
    test_user = pd.read_csv(FIRST_MATCH_TEST_USER)

    train_user = train_user[['phone_no_m', 'city_name', 'county_name', 'idcard_cnt', 'arpu_202003', "label"]].copy()
    train_user.columns = ['phone_no_m', 'city_name', 'county_name', 'idcard_cnt', 'arpu', 'label']
    train_user["month"] = ["3"]*len(train_user)

    test_user.columns = ['phone_no_m', 'city_name', 'county_name', 'idcard_cnt', 'arpu']
    test_user = test_user.join(fir_match_result.set_index(["phone_no_m"]), on=["phone_no_m"])
    test_user["month"] = ["4"]*len(test_user)

    user = train_user.append(test_user)
    user.to_excel("Data/rematch/train_user.xlsx", index=False)


# 合并短信数据
def merge_sms_data():
    train_sms = pd.read_excel(FIRST_MATCH_TRAIN_SMS)
    test_sms = pd.read_csv(FIRST_MATCH_TEST_SMS)
    sms = train_sms.append(test_sms)
    sms.to_csv("Data/rematch/train_sms.csv", index=None)


# 合并通话记录
def merge_voc_data():
    train_voc = pd.read_excel(FIRST_MATCH_TRAIN_VOC)
    test_voc = pd.read_csv(FIRST_MATCH_TEST_VOC)
    voc = train_voc.append(test_voc)
    voc.to_csv("Data/rematch/train_voc.csv", index=None)

# 合并APP数据
def merge_app_data():
    train_app = pd.read_excel(FIRST_MATCH_TRAIN_APP)
    test_app = pd.read_csv(FIRST_MATCH_TEST_APP)
    app = train_app.append(test_app)
    app.to_csv("Data/rematch/train_app.csv", index=False)

if __name__ == '__main__':
    if not os.path.exists("Data/rematch"):
        os.makedirs("Data/rematch")

    merge_user_data()
    merge_sms_data()
    merge_voc_data()
    merge_app_data()
