# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/14 15:15
# IDE：PyCharm

from Tools.data import get_train_test_data
import pandas as pd
from pandas.api.types import is_int64_dtype, is_float_dtype

if __name__ == '__main__':
    # 获取训练集、测试集数据
    train_data, test_data = get_train_test_data()

    # 2569个欺诈用户，5582个正常用户。总共8151个用户
    train_data["label"].value_counts()

    # 913个用户ARPU为0，且全部为欺诈用户。
    train_data[train_data["arpu"] == 0]["label"].value_counts()
    # 去除这913个用户之后，仍剩下7238个用户。其中1656个欺诈用户，5582个正常用户
    except_arpu_data = train_data[train_data.apply(lambda x: False if x["arpu"] == 0 else True, axis=1)].copy()
    except_arpu_data["label"].value_counts()
    except_arpu_data[except_arpu_data["flow"] == 0]["label"].value_counts()

    # 43个用户的arpu大于等于550，且全部为欺诈用户。
    except_arpu_data[except_arpu_data["arpu"] >= 550]["label"].value_counts()
    # 剩下7238-43=7195个用户
    except_arpu_data = except_arpu_data[except_arpu_data["arpu"] < 550]

    # 当天最多与135个及以上的不同用户进行过通话。有78个用户，且全部为欺诈用户
    except_arpu_data[except_arpu_data["voc_inner_day_user_cnt_max"] >= 135]["label"].value_counts()
    # 剩下7195-78=7117个用户
    except_arpu_data = except_arpu_data[except_arpu_data["voc_inner_day_user_cnt_max"] < 135]

    #
    except_arpu_data[except_arpu_data["passive_voc_inner_hour_cnt_max"]>30]["label"].value_counts()

    dtypes_all = except_arpu_data.dtypes
    for column in except_arpu_data.columns:
        if is_float_dtype(dtypes_all[column]) or (is_int64_dtype(dtypes_all[column])):
            temp_statistic = except_arpu_data[except_arpu_data[column] == 0]["label"].value_counts()
            if len(temp_statistic) == 1:
                print("--- " + column)
                print(temp_statistic)
