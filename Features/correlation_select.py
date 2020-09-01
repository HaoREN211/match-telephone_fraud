# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/9 11:52
# IDE：PyCharm

from Tools.functions import *

if __name__ == '__main__':
    train_data = pd.read_excel("data_train.xlsx", header=0)
    test_data = pd.read_excel("data_test.xlsx", header=0)

    columns = find_best_columns_by_correlation(train_data, "label", threshold_filtration=0.1, threshold_inter=0.5)

    result = pd.DataFrame(columns=["threshold_filtration", "threshold_inter", "accuracy", "columns"])
    model = XGBClassifier()
    for i in range(10, 80, 10):
        threshold_filtration = i/100
        for j in range(10,100,10):
            threshold_inter = j/100
            columns = find_best_columns_by_correlation(train_data, "label",
                                                       threshold_filtration=threshold_filtration,
                                                       threshold_inter=threshold_inter)
            if len(columns)>=10:
                accuracy = verify_model_accuracy(model, train_data, columns, "label")
                result = result.append(pd.DataFrame({
                    "threshold_filtration": [threshold_filtration],
                    "threshold_inter": [threshold_inter],
                    "accuracy": [accuracy],
                    "columns": [",".join(columns)]
                }))
    result.sort_values(by=["accuracy"], ascending=False, inplace=True)
    columns = find_best_columns_by_correlation(train_data, "label",
                                               threshold_filtration=0.1,
                                               threshold_inter=0.9)