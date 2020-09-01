# @Time    : 2020/6/17 20:37
# @Author  : REN Hao
# @FileName: main.py
# @Software: PyCharm

from Main import pd, np, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve, auc, roc_auc_score
from joblib import dump, load

if __name__ == '__main__':
    # 如果存在已有的模型，则加载模型，不用再重构训练集，训练模型
    if os.path.exists("forest_model.joblib"):
        forest_model = load('forest_model.joblib')
    else:
        # 如果训练存在的话训练模型
        if os.path.exists(r"train_data.xlsx"):
            data = pd.read_excel(r"train_data.xlsx", header=0)

            X = data[['voc_user_cnt', 'voc_user_min_cnt',
                   'voc_user_mean_cnt', 'voc_user_std_cnt', 'user_max_cnt_inner_day',
                   'user_min_cnt_inner_day', 'max_cnt_inner_day', 'min_cnt_inner_day',
                   'voc_cnt_per_user', 'call_type_1_ratio', 'call_type_2_ratio',
                   'idcard_cnt', 'sms_type_1_ratio', 'sms_type_2_ratio', 'sms_cnt',
                   'app_cnt', 'flow', 'fake_ratio'
            ]]
            y = data["label"].values

            train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)
            forest_model = RandomForestRegressor(random_state=1)
            forest_model.fit(train_X, train_y)
            melb_preds = forest_model.predict(val_X)

            dump(forest_model, "forest_model.joblib")

            # 计算各threshold对应的fpr，tpr
            fpr, tpr, threshold = roc_curve(val_y, melb_preds)
            roc_auc = auc(fpr, tpr)

            nb_sample = len(melb_preds)
            result_pd = pd.DataFrame(columns=["threshold", "precision"])

            for i in range(100):
                thres = (i+1)/100.0
                y_predict = [1 if x>=thres else 0 for x in melb_preds]
                result = sum([1 if val_y[x]==y_predict[x] else 0 for x in range(nb_sample)])/nb_sample
                result_pd = result_pd.append({"threshold":[thres], "precision": [result]}, ignore_index=True)

            ### 随机森林分类器
            rf0 = RandomForestClassifier(oob_score=True, random_state=12)
            rf0.fit(X, y)
            y_predprob = rf0.predict_proba(val_X)[:, 1]
            roc_auc_score(val_y, y_predprob)
            dump(forest_model, "y_random_forest_classifier.joblib")
    # 对随机森林分类器进行网格优化
    ### 对n_estimators进行网格搜索
    param_test1 = {'n_estimators': [50, 120, 160, 200, 250]}
    gsearch1 = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,
                                                             min_samples_leaf=20, max_depth=8, max_features='sqrt',
                                                             random_state=10),
                            param_grid=param_test1, scoring='roc_auc', cv=5)


    test_data = pd.read_excel("test_data.xlsx", header=0)
    test_X = test_data[['voc_user_cnt', 'voc_user_min_cnt',
              'voc_user_mean_cnt', 'voc_user_std_cnt', 'user_max_cnt_inner_day',
              'user_min_cnt_inner_day', 'max_cnt_inner_day', 'min_cnt_inner_day',
              'voc_cnt_per_user', 'call_type_1_ratio', 'call_type_2_ratio',
              'idcard_cnt', 'sms_type_1_ratio', 'sms_type_2_ratio', 'sms_cnt',
              'app_cnt', 'flow', 'fake_ratio'
              ]]
    test_preds = forest_model.predict(test_X)
    result = [1 if x >= 0.47 else 0 for x in test_preds]
    final_result = pd.DataFrame({
        "phone_no_m": test_data["phone_no_m"].values,
        "label": result
    })
    final_result.to_csv(r"", index=None)
