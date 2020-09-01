# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/17 14:56
# IDE：PyCharm

from Tools.data import get_train_test_data
from Features.rematch_features import RematchConfig
from Tools.functions import generate_target_data
import pandas as pd
from copy import copy

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data, final_test_data = get_train_test_data()
    self = RematchConfig()

    # 通话记录和短信记录中有很多重复的数据
    len(self.voc)
    len(self.voc.drop_duplicates(subset=["phone_no_m", "opposite_no_m", "calltype_id", "start_datetime"], keep="first"))

    generate_target_data(self,
                         "2303b7c370a7a60d5f0e113dd0fa15b16d2acd01f9aab092151d4ba158a14e87fdeb7bee2ef7f0e64388d3ec013ba807493489584d1b4b37b664a5cb83df0ffb")
    generate_target_data(self,
                         "e38ee69f77d942aa45e81ec7da9f5948ac527b081f3af9e78f348fee944926fc0a644cc88cbec3e05c1976b7f2c8f1f6e153a96871abad25a7ee3a566352df5d")
    generate_target_data(self,
                         "cdf8b5f08bd0a8e3c08fc58b394bc1146a8ebee636b80881666df5d503594d757c2b3b4429a01a3f50b62d7b372f8df6524f35549925ae5a39e31535c3431820")

    generate_target_data(self,
                         "fae2d9bc5bc2cb2869c39549f86e92341e95da16772cb39a2cbbb29583135f18638e3f15e95df5b53643520a9999a88c30f901177528c628f27d2ce99aea5506")
    generate_target_data(self,
                         "2afda98143a46e03484151d1714f2ba6ca06f91fb260dc273a115513b4305901e53959b9686a34e477785f369c993bf80205a68c2f13aa897214e77bfd081d75")
    # 好用户，一个月消费107块，但是没有任何短信、电话、app数据
    generate_target_data(self,
                         "2b06266c22f84c1c0ddb60e791ce2213406f58138fc4d1c1c438ebfeaf88e3816c4dda9c86152c183408fe32df86fa4c9c10edd00421c1cb6706fbe06de1bfd0")

    # 有短信记录，但是没有主动发送短信的记录
    train_data[(train_data["sms_cnt"] > 0) & (train_data["initiative_sms_cnt"] == 0)]["label"].value_counts()

    # https流量过高
    temp_data = self.app[self.app["busi_name"] == "HTTPS"].groupby("phone_no_m").agg(flow=("flow", pd.Series.sum))
    temp_data = self.user[["phone_no_m", "label"]].join(temp_data, on=["phone_no_m"]).fillna(0)
    temp_data[temp_data["flow"] >= 5000]["label"].value_counts()

    # 没有任何操作
    self.data[(self.data["sms_cnt"] == 0) & (self.data["voc_call_cnt"] == 0)
              & (self.data["arpu"] != 0) & (self.data["app_cnt"] != 0)]["label"].value_counts()

    # 短信和电话中对方均有打过来的记录，但是没有回复的内容
    columns = ["phone_no_m", "opposite_no_m", "calltype_id"]
    temp_data = self.voc[columns].drop_duplicates().copy()
    temp_data["type"] = ["c"] * len(temp_data)
    temp_data_1 = self.sms[columns].drop_duplicates().copy()
    temp_data_1["type"] = ["s"] * len(temp_data_1)

    temp_data = temp_data.append(temp_data_1).reset_index(drop=True)
    del temp_data_1

    temp_data["initiative_call"] = temp_data.apply(
        lambda x: 1 if ((x["calltype_id"] == 1) and (x["type"] == "c")) else 0, axis=1
    )
    temp_data["passive_call"] = temp_data.apply(
        lambda x: 1 if ((x["calltype_id"] == 2) and (x["type"] == "c")) else 0, axis=1
    )
    temp_data["initiative_sms"] = temp_data.apply(
        lambda x: 1 if ((x["calltype_id"] == 1) and (x["type"] == "s")) else 0, axis=1
    )
    temp_data["passive_sms"] = temp_data.apply(
        lambda x: 1 if ((x["calltype_id"] == 2) and (x["type"] == "s")) else 0, axis=1
    )

    agg_data = temp_data.groupby(["phone_no_m", "opposite_no_m"]).agg(
        initiative_call=("initiative_call", pd.Series.sum)
        , passive_call=("passive_call", pd.Series.sum)
        , initiative_sms=("initiative_sms", pd.Series.sum)
        , passive_sms=("passive_sms", pd.Series.sum)
    ).reset_index()

    agg_data["is_hit"] = agg_data.apply(
        lambda x: 1 if ((x["initiative_call"] == 0) & (x["passive_call"] > 0) & (x["initiative_sms"] == 0) & (
                    x["passive_sms"] > 0))
        else 0, axis=1
    )

    more_agg_data = agg_data.groupby("phone_no_m").agg(is_his=("is_hit", pd.Series.sum)).reset_index()
    more_agg_data = more_agg_data[more_agg_data["is_his"] > 0].join(
        self.user[["phone_no_m", "label"]].set_index("phone_no_m"), on=["phone_no_m"]
    ).copy()
    more_agg_data["label"].value_counts()

    # 只有一条通话记录
    self.data[self.data["voc_call_cnt"] == 1]["label"].value_counts()

    # 只有一条短信记录
    self.data[self.data["sms_cnt"] == 1]["label"].value_counts()

    # 探索还有没有能做成规则的特征，某个特征大于某个值的时候会不会全是欺诈电话。
    result = pd.DataFrame(columns=["feature", "threshold", "nb_faker"])
    column_out = ["phone_no_m", "label"]
    for current_column in self.data.columns:
        if current_column in column_out:
            continue
        print(current_column)
        current_threshold, nb_faker = None, 0

        for current_value in sorted(list(set([int(x * 100) / 100 for x in self.data[current_column].values])),
                                    reverse=True):
            current_sub_df = self.data[self.data[current_column] >= current_value]
            nb_good = len(current_sub_df[current_sub_df["label"] == 0])

            # 如果当前误杀了好用户，则取消迭代
            if nb_good > 0:
                break

            current_threshold = copy(current_value)
            nb_faker = len(current_sub_df[current_sub_df["label"] == 1])

        if nb_faker > 0:
            result = result.append(pd.DataFrame({
                "feature": [current_column]
                , "threshold": [current_threshold]
                , "nb_faker": [nb_faker]
            }))
    result.to_excel("fakser_rules.xlsx", index=None)
