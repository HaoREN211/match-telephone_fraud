# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/15 10:28
# IDE：PyCharm

import pandas as pd
from Features.rematch_features import RematchConfig

if __name__ == '__main__':
    self = RematchConfig()

    # 高危电话列表
    temp_data = self.voc[["phone_no_m", "opposite_no_m"]].drop_duplicates().join(
        self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]
    ).copy()

    agg_data = temp_data.groupby("opposite_no_m").agg(
        user_cnt = ("phone_no_m", pd.Series.count),
        risk_user_cnt = ("label", pd.Series.sum)
    ).reset_index()

    agg_data["risk_user_ratio"] = agg_data.apply(lambda x: round(x["risk_user_cnt"]/x["user_cnt"], 2), axis=1)
    high_risk_phone = list(set(agg_data[(agg_data["risk_user_ratio"] >= 0.99) & (agg_data["user_cnt"] >=3)]["opposite_no_m"].values))
    agg_data.to_excel("high_risk_opposite.xlsx", index=None)



