# @Time    : 2020/6/17 20:11
# @Author  : REN Hao
# @FileName: __init__.py.py
# @Software: PyCharm


# 获取用户的标签
tmp_data[["phone_no_m", "busi_name"]].dropna(subset=["busi_name"]).join(self.train_user[["phone_no_m", "label"]].set_index("phone_no_m"), on="phone_no_m")
fake_data = tmp_data[tmp_data["label"]==1]
fake_data = fake_data[["busi_name", "phone_no_m"]].drop_duplicates().groupby(["busi_name"]).count()
fake_data.columns = ["user_cnt"]
fake_data.sort_values(by=["user_cnt"], ascending=False)
fake_data = fake_data.reset_index()
fake_data.to_excel(r"fake_apps.xlsx", index=None)

normal_data = tmp_data[tmp_data["label"]==0][["busi_name", "phone_no_m"]].drop_duplicates().groupby(["busi_name"]).count()
normal_data.columns = ["user_cnt"]
normal_data = normal_data.sort_values(by=["user_cnt"], ascending=False).reset_index()
normal_data.to_excel("normal_apps.xlsx", index=None)