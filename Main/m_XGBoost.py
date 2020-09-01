# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/27 15:04
# IDE：PyCharm

from sklearn.model_selection import GridSearchCV
from Features.XGBoost_feature_selection import *
import xgboost as xgb
from xgboost import plot_tree
import matplotlib.pyplot as plt
from Tools.data import get_train_test_data
from sklearn.model_selection import KFold
from Tools.feature_selection import research_feature_by_forward_backward_search, research_feature_by_backward_search

if __name__ == '__main__':
    train_data, tmp_test_data, final_test_data = get_train_test_data()
    columns = select_features(train_data=train_data,
                              drop_columns=["phone_no_m", "label"],
                              label_name="label")

    X, y, test_X = train_data[columns], train_data["label"].values, tmp_test_data[columns]
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

    # 验证模型的好坏
    model = XGBClassifier()

    new_columns = research_feature_by_forward_backward_search(train_data, [], drop_columns=["phone_no_m", "label"],
                                                              model=model)
    back_forward_columns = research_feature_by_backward_search(train_data, train_data.drop(columns=["phone_no_m", "label"]).columns)

    model.fit(train_X, train_y)
    val_y_predict = model.predict(val_X)
    print(accuracy_score(val_y, val_y_predict))

    # 交叉验证，对训练集中所有的样本进行预测。用于bagging聚合模型用
    kf = KFold(n_splits=10, shuffle=True, random_state=0)
    result_predict = pd.DataFrame(columns=["phone_no_m", "label"])
    for train_index, test_index in kf.split(train_data):
        temp_train_data, temp_test_data = train_data.loc[train_index, :], train_data.loc[test_index, :]
        temp_train_X, temp_train_y = temp_train_data[columns], temp_train_data["label"].values
        temp_test_X = temp_test_data[columns]

        model = XGBClassifier()
        model.fit(temp_train_X, temp_train_y)
        result_predict = result_predict.append(pd.DataFrame({
            "phone_no_m": temp_test_data["phone_no_m"].values,
            "label": model.predict(temp_test_X)
        }))
    result_predict.reset_index(drop=True).to_csv("z_xgboost_train.csv", index=False)

    # 验证预测结果
    result_predict.columns = ["phone_no_m", "label_predict"]
    result_predict = train_data[["phone_no_m", "label"]].join(result_predict.set_index("phone_no_m"), on="phone_no_m")
    print(accuracy_score(result_predict["label"].values.tolist(), result_predict["label_predict"].values.tolist()))

    model.fit(X, y)

    # 可视化xgboost决策
    plt.figure(figsize=(15, 9))
    xgb.to_graphviz(model)
    plt.show()
    plot_tree(model)

    digraph = xgb.to_graphviz(model, num_trees=2)
    digraph.format = 'png'
    digraph.view('./ttiris_xgb')

    result_check = pd.DataFrame({
        "phone_no_m": val_X["phone_no_m"].values,
        "label": val_y,
        "predict": val_y_predict
    })

    result_check.to_excel("result_check.xlsx", index=None)

    model.fit(X, y)
    test_y = model.predict(test_X)
    final_result = final_test_data.append(
        pd.DataFrame({
            "phone_no_m": tmp_test_data["phone_no_m"].values,
            "label": test_y
        })
    )
    final_result.to_csv("z_xgboost.csv", index=None)

    # 将当前入模的特征保存下来，并存入本地文件
    df_columns = pd.DataFrame({"columns": columns})
    df_columns.to_excel("z_xgboost_columns.xlsx", index=None)

    columns_df = pd.DataFrame({"columns": columns})
    columns_df.to_excel("Submit/rank_16_columns.xlsx", index=None)

    # 调参
    parameters = {
        # 给定数的深度，默认为3
        'max_depth': [3, 4, 5],

        # 每个迭代产生的模型的权重、学习率，默认为0.1
        'learning_rate': [0.01],

        # 子模型的数量，默认为100
        'n_estimators': [50],

        'min_child_weight': [0, 2],
        'max_delta_step': [0],

        # 这个参数控制对于每棵树，随机采样的比例。减小这个参数的值，算法会更加保守，避免过拟合。
        # 但是，如果这个值设置得过小，它可能会导致欠拟合。
        # 典型值：0.5-1，0.5代表平均采样，防止过拟合. 范围: (0,1]，注意不可取0
        'subsample': [0.7],

        # 给定模型的求解方式
        'booster': ["gbtree", "gblinear"],
        'colsample_bytree': [0.6],

        # l1正则项的权重，默认为0
        'reg_alpha': [0.25],

        # l2正则项的权重，默认为1
        'reg_lambda': [0.4],
        'scale_pos_weight': [0.4]
    }

    parameters = {
        # 给定数的深度，默认为3
        'max_depth': [6],
        # 'max_depth': [7],
        # 每个迭代产生的模型的权重、学习率，默认为0.1
        'learning_rate': [0.09],
        # 'learning_rate': [0.09],
        # 子模型的数量，默认为100
        'n_estimators': [148],
        # 这个参数控制对于每棵树，随机采样的比例。减小这个参数的值，算法会更加保守，避免过拟合。
        # 但是，如果这个值设置得过小，它可能会导致欠拟合。
        # 典型值：0.5-1，0.5代表平均采样，防止过拟合. 范围: (0,1]，注意不可取0
        'subsample': [0.68],
        # 'subsample': [0.7],
        # 给定模型的求解方式
        # 'booster': ["gbtree", "gblinear"],
        # l1正则项的权重，默认为0
        'reg_alpha': [0.09],
        # 'reg_alpha': [0.1],
    }

    xlf = XGBClassifier()
    gsearch = GridSearchCV(xlf, param_grid=parameters, scoring='accuracy', cv=3)
    gsearch.fit(X, y)
    gsearch.best_params_

    # 计算相关性
    train_corr = train_data.corr()["label"]
    df_train_corr = pd.DataFrame({"column": train_corr.index,
                                  "correlation": train_corr.values,
                                  "correlation_abs": [abs(x) for x in train_corr.values]})
    df_train_corr.sort_values(by=["correlation_abs"], ascending=False, inplace=True)
    df_train_corr.drop(index=df_train_corr[df_train_corr["column"] == "label"].index, inplace=True)
