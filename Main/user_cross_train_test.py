# @Time    : 2020/7/1 20:19
# @Author  : REN Hao
# @FileName: user_cross_train_test.py
# @Software: PyCharm

import pandas as pd

if __name__ == '__main__':
    train_file = r"C:\Project\Python\match-telephone_fraud\Data\train\train_user.csv"
    test_file = r"C:\Project\Python\match-telephone_fraud\Data\test\test_user.csv"

    train_user = pd.read_csv(train_file, header=0)
    test_user = pd.read_csv(test_file, header=0)[["phone_no_m", "arpu_202004"]]
    train_user[["phone_no_m", "label"]].join(test_user.set_index("phone_no_m"),
                                             on="phone_no_m", how="left")
