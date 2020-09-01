# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/11 10:55
# IDE：PyCharm

from sklearn.feature_selection import SelectKBest ,chi2
import pandas as pd

if __name__ == '__main__':
    train_data = pd.read_excel("data_train.xlsx", header=0)
    test_data = pd.read_excel("data_test.xlsx", header=0)
    # 选择相关性最高的前5个特征
    X_chi2 = SelectKBest(chi2, k=20).fit_transform(train_data.drop(columns=["phone_no_m", "label"
        , "call_activate_days_diff", "sms_activate_days_diff", "arpu"]), train_data["label"])
    X_chi2 = SelectKBest(chi2, k=20).fit(train_data.drop(columns=["phone_no_m", "label"
        , "call_activate_days_diff", "sms_activate_days_diff", "arpu"]), train_data["label"])
    X_chi2.shape
