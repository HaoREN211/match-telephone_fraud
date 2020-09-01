# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/7 14:28
# IDE：PyCharm
# https://zhuanlan.zhihu.com/p/121799598

from Tools.data import get_train_test_data
import toad
from toad.plot import bin_plot

if __name__ == '__main__':
    train_data, test_data = get_train_test_data()

    # 返回每个特性的EDA报告，包括数据类型、分布、缺失率和惟一值。
    toad_detector = toad.detector.detect(train_data)

    # 下面以缺失率大于0.5.IV值小于0.05或者相关性大于0.9(保留较高的特征)来进行特征筛选。
    selected_data, drop_lst = toad.selection.select(train_data,
                                                    target='label', empty=0.5, iv=0.05, corr=0.9,
                                                    return_drop=True, exclude=['phone_no_m'])

    # 返回每个特征的质量，包括iv、基尼系数和熵。可以帮助我们发现更有用的潜在信息。
    quality = toad.quality(selected_data, 'label')

    # 对数值型和类别型变量进行分箱，支持决策树分箱、卡方分箱、最优分箱等
    # 初始化一个combiner类
    combiner = toad.transform.Combiner()
    # 训练数据并指定分箱方法，其它参数可选。分箱阈值的方法（method） 包括：'chi','dt','quantile','step','kmeans'
    combiner.fit(selected_data, y='label', method='chi', min_samples=0.05, exclude='phone_no_m')
    # 以字典形式保存分箱结果
    bins = combiner.export()
    # 查看某特征的分箱区间值
    print(bins["arpu"])
    # 进行分箱转化
    selected_data_transformed = combiner.transform(selected_data)
    quality_transformed = toad.quality(selected_data_transformed, 'label')

    # 分箱后通过画图观察
    bin_plot(selected_data_transformed, x='arpu', target='label')
