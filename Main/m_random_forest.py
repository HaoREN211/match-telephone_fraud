# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/29 11:41
# IDE：PyCharm

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from Features.XGBoost_feature_selection import *
from Tools.data import get_train_test_data
from sklearn.model_selection import KFold
from Tools.feature_selection import research_feature_by_forward_backward_search

if __name__ == '__main__':
    # 加载训练集和待测试的数据
    train_data, test_data, final_test_data = get_train_test_data()

    # 通过随机森林筛选特征
    rf0 = RandomForestClassifier(oob_score=True, random_state=12)
    columns = select_features(train_data=train_data,
                              drop_columns=["phone_no_m", "label"],
                              label_name="label", model=rf0)
    new_columns = research_feature_by_forward_backward_search(train_data, [], drop_columns=["phone_no_m", "label"], model=rf0)
    df_columns = pd.DataFrame({"columns": columns})
    df_columns.to_csv("z_random_forest_column.csv", index=False)

    # 交叉验证，对训练集中所有的样本进行预测。用于bagging聚合模型用
    kf = KFold(n_splits=10, shuffle=True, random_state=0)
    result_predict = pd.DataFrame(columns=["phone_no_m", "label"])
    for train_index, test_index in kf.split(train_data):
        temp_train_data, temp_test_data = train_data.loc[train_index, :], train_data.loc[test_index, :]
        temp_train_X, temp_train_y = temp_train_data[columns], temp_train_data["label"].values
        temp_test_X = temp_test_data[columns]

        rf0 = RandomForestClassifier(oob_score=True, random_state=12)
        rf0.fit(temp_train_X, temp_train_y)
        result_predict = result_predict.append(pd.DataFrame({
            "phone_no_m": temp_test_data["phone_no_m"].values,
            "label": rf0.predict(temp_test_X)
        }))
    result_predict.reset_index(drop=True).to_csv("z_random_forest_train.csv", index=False)

    X = train_data[columns]
    y = train_data["label"].values
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

    rf0.fit(train_X, train_y)
    val_y_pre = rf0.predict(val_X)
    print(accuracy_score(val_y, val_y_pre))

    val_y_prob = rf0.predict_proba(val_X)[:,1]
    # 0.968010119497866
    roc_auc_score(val_y, val_y_prob)


    # 1. 首先对n_estimators进行网格搜索：
    param_test1 = {'n_estimators': [1, 10, 50, 120, 160, 200, 250]}
    gsearch1 = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,
                                                             min_samples_leaf=20, max_depth=8, max_features='sqrt',
                                                             random_state=10),
                            param_grid=param_test1, scoring='roc_auc', cv=5)
    gsearch1.fit(train_X, train_y)
    best_n_estimators = 50

    # 2. 接着我们对决策树最大深度max_depth进行网格搜索。
    param_test2 = {'max_depth': [1, 2, 3, 5, 7, 9, 10, 11, 12, 13]}
    gsearch2 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=best_n_estimators, min_samples_split=100,
                                                             min_samples_leaf=20, max_features='sqrt', oob_score=True,
                                                             random_state=10),
                            param_grid=param_test2, scoring='roc_auc', cv=5)
    gsearch2.fit(train_X, train_y)
    best_max_depth = 10

    # 3. 接着我们对决策树内部节点再划分所需最小样本数min_samples_split进行网格搜索。
    param_test3 = {'min_samples_split': [45,46,47,48,49,50,51,52,53,54,55]}
    gsearch3 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=best_n_estimators, max_depth=best_max_depth,
                                                             min_samples_leaf=20, max_features='sqrt', oob_score=True,
                                                             random_state=10),
                            param_grid=param_test3, scoring='roc_auc', cv=5)
    gsearch3.fit(train_X, train_y)
    best_min_samples_split = 47

    rf1 = RandomForestClassifier(n_estimators=best_n_estimators,
                                 max_depth=best_max_depth,
                                 min_samples_split=best_min_samples_split, min_samples_leaf=20,
                                 max_features='sqrt', oob_score=True, random_state=10)
    rf1.fit(train_X, train_y)
    val_y_prob_1 = rf1.predict_proba(val_X)[:, 1]
    # 调参之后验证集的roc_auc_score得分变低了，现在从新进行验证
    roc_auc_score(val_y, val_y_prob_1)

    ### 这一次同时对所有的参数进行网格搜索
    param_test_all = {
        'n_estimators': [50, 120, 160, 200, 250],
        'max_depth': [1, 2, 3, 5, 7, 9, 11, 13],
        'min_samples_split': [50, 80, 100, 120, 150, 180, 200, 300],
        'min_samples_leaf': [10, 20, 30, 40, 50, 100],
        'max_features': [3, 5, 7, 9, 11]
    }
    gsearch = GridSearchCV(estimator=RandomForestClassifier(oob_score=True, random_state=10),
                            param_grid=param_test_all, scoring='roc_auc', cv=5)
    gsearch.fit(train_X, train_y)

    rf0.fit(X, y)
    val_y_pre = rf0.predict(val_X)
    accuracy_score(val_y, val_y_pre)
    roc_auc_score(val_y, val_y_pre)

    final_result = pd.DataFrame({
        "phone_no_m": test_data["phone_no_m"].values,
        "label": rf0.predict(test_data[columns])
    })
    final_result_df = final_test_data.append(final_result)
    final_result_df.to_csv(r"z_random_forest.csv", index=None)

    # 将当前入模的特征保存下来，并存入本地文件
    df_columns = pd.DataFrame({"columns": columns})
    df_columns.to_excel("z_random_forest_columns.xlsx", index=None)
