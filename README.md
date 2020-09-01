# match-telephone_fraud

[比赛链接](http://www.scdata.net.cn/common/cmpt/%E8%AF%88%E9%AA%97%E7%94%B5%E8%AF%9D%E8%AF%86%E5%88%AB_%E6%8E%92%E8%A1%8C%E6%A6%9C.html)


### 相关调查资料
|中文名|链接|
|:--|:--|
|2016诈骗电话态势与特征分析报告|[链接](https://www.docin.com/p-1808789621.html)|
|诈骗电话特征分析及其拦截手段研究与设计实践|[链接](http://www.doc88.com/p-2611795104925.html)|

### 去除重复数据

经过调查发现，通话记录和短信记录中存在冗杂数据的情况。相同两个用户在同一时刻有时会产生两条相同的短信记录，或区域不同的通话数据。后者可能是在通话过程中，用户所在区域发生了变化导致的。

### 使用部分特征作为规则

对命中以下规则的样本，不放入模型训练，也不使用模型预测其标签，而是直接判定为欺诈电话：

1. 当月消费为0的用户，即arpu=0；
1. 当月消费过高的用户，即arpu>=550的用户；
1. 主呼通话记录中，出现的用户数过多，即initiative_voc_user_cnt大于1275的用户；
1. 一天的通话记录中，出现的用户数过多，即voc_inner_day_user_cnt_max大于等于135；


相关系数

短信各时间段的发送与接收总次数与通话记录一样，与标签没有明显的相关性

|列名|中文解释|config里对应的函数|与label的相关系数|
|:--|:--|:--|:--|
|voc_cnt|通话记录次数|get_voc_cnt()|-0.033776|
|voc_user_cnt|通话记录中的通话人数|get_voc_opposite_user_cnt()|0.207425|
|voc_user_max_cnt|与同一个人通话的最大通话次数|get_voc_user_max_min_cnt()|-0.046010|
|voc_user_min_cnt|与同一个人通话的最小通话次数|get_voc_user_max_min_cnt()|-0.273632|
|voc_user_mean_cnt|与同一个人通话的平均次数|get_voc_user_max_min_cnt()|-0.370789|
|voc_user_median_cnt|与同一个人通话的中位数|get_voc_user_max_min_cnt()|-0.121849|
|voc_user_std_cnt|与同一个人通话的方差|get_voc_user_max_min_cnt()|-0.368735|
|user_max_cnt_inner_day|一天中与不同用户拨打电话的最大用户数|get_voc_user_inner_day()|0.522207|
|user_min_cnt_inner_day|一天中与不同用户拨打电话的最小用户数|get_voc_user_inner_day()|0.282751|
|max_cnt_inner_day|一天中最大拨打次数|get_voc_cnt_inner_day()|0.488075|
|min_cnt_inner_day|一天中最小拨打次数|get_voc_cnt_inner_day()|0.298768|
|dur_max|通话最长时长|get_voc_duration_indicator()|-0.010817|
|dur_min|通话最短时长|get_voc_duration_indicator()|0.032581|
|dur_median|通话时长中位数|get_voc_duration_indicator()|0.037360|
|dur_mean|通话时长平均数|get_voc_duration_indicator()|0.097072|
|dur_std|通话时长方差|get_voc_duration_indicator()|0.117692|
|interval_0_cnt|0点通话次数|get_voc_time_interval_ratio()|0.018223|
|interval_1_cnt|1点通话次数|get_voc_time_interval_ratio()|0.033306|
|interval_2_cnt|2点通话次数|get_voc_time_interval_ratio()|0.029925|
|interval_3_cnt|3点通话次数|get_voc_time_interval_ratio()|0.028222|
|interval_4_cnt|4点通话次数|get_voc_time_interval_ratio()|-0.017755|
|interval_5_cnt|5点通话次数|get_voc_time_interval_ratio()|-0.075354|
|interval_6_cnt|6点通话次数|get_voc_time_interval_ratio()|-0.131857|
|interval_7_cnt|7点通话次数|get_voc_time_interval_ratio()|-0.198584|
|interval_8_cnt|8点通话次数|get_voc_time_interval_ratio()|-0.134073|
|interval_9_cnt|9点通话次数|get_voc_time_interval_ratio()|0.029675|
|interval_10_cnt|10点通话次数|get_voc_time_interval_ratio()|0.099223|
|interval_11_cnt|11点通话次数|get_voc_time_interval_ratio()|0.095168|
|interval_12_cnt|12点通话次数|get_voc_time_interval_ratio()|0.018737|
|interval_13_cnt|13点通话次数|get_voc_time_interval_ratio()|0.091377|
|interval_14_cnt|14点通话次数|get_voc_time_interval_ratio()|0.148943|
|interval_15_cnt|15点通话次数|get_voc_time_interval_ratio()|0.160256|
|interval_16_cnt|16点通话次数|get_voc_time_interval_ratio()|0.148433|
|interval_17_cnt|17点通话次数|get_voc_time_interval_ratio()|0.086431|
|interval_18_cnt|18点通话次数|get_voc_time_interval_ratio()|-0.023021|
|interval_19_cnt|19点通话次数|get_voc_time_interval_ratio()|-0.060203|
|interval_20_cnt|20点通话次数|get_voc_time_interval_ratio()|-0.083821|
|interval_21_cnt|21点通话次数|get_voc_time_interval_ratio()|-0.077684|
|interval_22_cnt|22点通话次数|get_voc_time_interval_ratio()|-0.053936|
|interval_23_cnt|23点通话次数|get_voc_time_interval_ratio()|-0.004354|
|interval_0_ratio|0点通话次数占比|get_voc_time_interval_ratio()|0.044429|
|interval_1_ratio|1点通话次数占比|get_voc_time_interval_ratio()|0.047716|
|interval_2_ratio|2点通话次数占比|get_voc_time_interval_ratio()|0.038376|
|interval_3_ratio|3点通话次数占比|get_voc_time_interval_ratio()|0.02585|
|interval_4_ratio|4点通话次数占比|get_voc_time_interval_ratio()|-0.014234|
|interval_5_ratio|5点通话次数占比|get_voc_time_interval_ratio()|-0.100607|
|interval_6_ratio|6点通话次数占比|get_voc_time_interval_ratio()|-0.218894|
|interval_7_ratio|7点通话次数占比|get_voc_time_interval_ratio()|-0.336745|
|interval_8_ratio|8点通话次数占比|get_voc_time_interval_ratio()|-0.149011|
|interval_9_ratio|9点通话次数占比|get_voc_time_interval_ratio()|-0.100539|
|interval_10_ratio|10点通话次数占比|get_voc_time_interval_ratio()|0.003209|
|interval_11_ratio|11点通话次数占比|get_voc_time_interval_ratio()|-0.015489|
|interval_12_ratio|12点通话次数占比|get_voc_time_interval_ratio()|-0.053589|
|interval_13_ratio|13点通话次数占比|get_voc_time_interval_ratio()|0.102556|
|interval_14_ratio|14点通话次数占比|get_voc_time_interval_ratio()|0.230686|
|interval_15_ratio|15点通话次数占比|get_voc_time_interval_ratio()|0.26821|
|interval_16_ratio|16点通话次数占比|get_voc_time_interval_ratio()|0.219702|
|interval_17_ratio|17点通话次数占比|get_voc_time_interval_ratio()|0.005557|
|interval_18_ratio|18点通话次数占比|get_voc_time_interval_ratio()|-0.160235|
|interval_19_ratio|19点通话次数占比|get_voc_time_interval_ratio()|-0.197138|
|interval_20_ratio|20点通话次数占比|get_voc_time_interval_ratio()|-0.186044|
|interval_21_ratio|21点通话次数占比|get_voc_time_interval_ratio()|-0.131538|
|interval_22_ratio|22点通话次数占比|get_voc_time_interval_ratio()|-0.087297|
|interval_23_ratio|23点通话次数占比|get_voc_time_interval_ratio()|0.004302|
|voc_cnt_per_user|与同一用户的平均通话次数|get_user_avg_voc_cnt()|-0.370789|
|call_type_1_cnt|用户主呼次数|get_voc_call_type_id()|0.070538|
|call_type_2_cnt|用户被呼次数|get_voc_call_type_id()|-0.183388|
|call_type_3_cnt|用户呼转次数|get_voc_call_type_id()|-0.013067|
|call_type_1_ratio|用户主呼占比|get_voc_call_type_id()|0.415467|
|call_type_2_ratio|用户被呼占比|get_voc_call_type_id()|-0.481819|
|call_type_3_ratio|用户呼转占比|get_voc_call_type_id()|0.000181|
|idcard_cnt|身份证下电话号码个数|idcard_cnt|0.400548|
|sms_cnt|短信总个数|get_sms_cnt()|-0.105734|
|call_type_1_cnt|发送短信总个数|get_sms_cnt()|0.126599|
|call_type_2_cnt|接收短信总个数|get_sms_cnt()|-0.207957|
|call_type_1_ratio|发送短信占比|get_sms_cnt()|0.346481|
|call_type_2_ratio|接收短信占比|get_sms_cnt()|-0.338402|
|...|各时间段的发送与接收次数及占比|get_sms_time_interval_ratio()|不明显|
|...|各周天主动拨打电话次数和占比|week_day_statistic()|不明显|
|app_cnt|app数量|app_cnt()|-0.28099|
|flow|流量|flow_cnt()|-0.14898|
|voc_6_cnt_max|六小时内最大通话记录数|six_hour_voc_cnt()|0.553170|
|voc_6_cnt_mean|六小时内平均通话记录数|six_hour_voc_cnt()|0.584181|
|voc_6_cnt_median|六小时内通话记录中位数|six_hour_voc_cnt()|0.547948|
|voc_6_cnt_std|六小时内通话记录方差|six_hour_voc_cnt()|0.574683|
|imei_cnt|imei的个数|voc_imei_cnt()|0.180026|
|black_app_cnt|高危APP的个数|get_white_black_app_cnt()|0.138217|
|white_app_cnt|白名单的个数|get_white_black_app_cnt()|-0.232684|
|active_days|活跃天数|active_days()|-0.534571|
|city_cnt|主呼城市数目|call_city_cnt()|-0.272559|
|call_interval_min|最小通话间隔|call_interval_cnt()|0.000426|
|call_interval_max|最大通话间隔|call_interval_cnt()|-0.431949|
|call_interval_mean|平均通话间隔|call_interval_cnt()|-0.578544|
|call_interval_median|通话间隔中位数|call_interval_cnt()|-0.366267|
|call_interval_std|通话间隔方差|call_interval_cnt()|-0.625256|
|initiative_call_interval_min|主动呼叫最小间隔|initiative_call_interval_cnt()|-0.016830|
|initiative_call_interval_max|主动呼叫最大间隔|initiative_call_interval_cnt()|-0.406209|
|initiative_call_interval_mean|主动呼叫平均间隔|initiative_call_interval_cnt()|-0.642805|
|initiative_call_interval_median|主动呼叫间隔中位数|initiative_call_interval_cnt()|-0.447079|
|initiative_call_interval_std|主动呼叫间隔方差|initiative_call_interval_cnt()|-0.657769|
|passive_call_interval_min|被动呼叫最小间隔|passive_call_interval_cnt()|0.091288|
|passive_call_interval_max|被动呼叫最大间隔|passive_call_interval_cnt()|-0.445002|
|passive_call_interval_mean|被动呼叫平均间隔|passive_call_interval_cnt()|-0.399951|
|passive_call_interval_median|被动呼叫间隔中位数|passive_call_interval_cnt()|-0.281940|
|passive_call_interval_std|被动呼叫间隔方差|passive_call_interval_cnt()|-0.418371|
|sms_type_1_user|发送短信的对方用户数|avg_sms_type_1_cnt_per_user()|0.128004|
|sms_type_1_cnt_per_user|与同一用户发送的平均短信数目|avg_sms_type_1_cnt_per_user()|0.007956|
|sms_type_1_min_cnt_per_interval|单一时间段发送的最小短信数目|avg_sms_type_1_cnt_per_interval()|0.054026|
|sms_type_1_max_cnt_per_interval|单一时间段发送的最大短信数目|avg_sms_type_1_cnt_per_interval()|0.152503|
|sms_type_1_avg_cnt_per_interval|单一时间段发送的平均短信数目|avg_sms_type_1_cnt_per_interval()|0.135658|
|sms_type_1_median_cnt_per_interval|单一时间段发送的短信数目中位|avg_sms_type_1_cnt_per_interval()|0.114401|
|sms_type_1_std_cnt_per_interval|单一时间段发送的短信数目方差|avg_sms_type_1_cnt_per_interval()|0.151362|
|initial_voc_county_cnt|主呼区域数量|county_cnt()|-0.309735|
|passive_voc_county|被呼区域数量|county_cnt()|-0.285208|
|turn_voc_county|呼转区域数量|county_cnt()|-0.028933|
|call_dur|通话总时长|voc_dur_info()|-0.042797|
|turn_call_dur|呼转通话总时长|voc_dur_info()|-0.008260|
|initial_call_dur|主动通话总时长|voc_dur_info()|0.059502|
|passive_call_dur|被动通话总时长|voc_dur_info()|-0.173036|
|passive_call_dur_ratio|被动通话时长占比|voc_dur_info()|-0.500371|
|initial_call_dur_ratio|主动通话时长占比|voc_dur_info()|-0.304476|
|turn_call_dur_ratio|呼转通话时长占比|voc_dur_info()|-0.003298|
|passive_call_daily_dur|平均每日被动电话通话时长|voc_dur_info()|-0.129877|
|initial_call_daily_dur|平均每日主动电话通话时长|voc_dur_info()|-0.226543|
|turn_call_daily_dur|平均每日呼转电话通话时长|voc_dur_info()|-0.000306|
|daily_call_type_1_cnt|平均每日主呼电话次数|voc_dur_info()|0.228135|
|daily_call_type_2_cnt|平均每日被呼电话次数|voc_dur_info()|-0.148405|
|daily_call_type_3_cnt|平均每日呼转电话次数|voc_dur_info()|-0.003932|
|2020年7月3日新加工特征| | | |
|multiple_initial_sms_cnt|同一时刻给同一用户发送两条及以上的短息次数|multiple_sms_cnt()|-0.006999|
|multiple_passive_sms_cnt|同一时刻接收同一用户发送两条及以上的短息次数|multiple_sms_cnt()|-0.298029|
|initiative_call_active_days|拨打电话的活跃天数|initiative_passive_activate_days_diff()|-0.458121|
|passive_call_active_days|接听电话的活跃天数|initiative_passive_activate_days_diff()|-0.445352|
|initiative_sms_active_days|发送短信的活跃天数|initiative_passive_activate_days_diff()|-0.043539|
|passive_sms_active_days|接收短信的活跃天数|initiative_passive_activate_days_diff()|-0.690040|
|call_activate_days_diff|拨打、接听电话的活跃天数差值|initiative_passive_activate_days_diff()|0.011568|
|sms_activate_days_diff|发送、接收短信的活跃天数差值|initiative_passive_activate_days_diff()|0.695105|
|interactive_call_user_cnt|通话记录中同时有拨打和接听的用户数|interactive_user_cnt()|-0.190232|
|interactive_sms_user_cnt|短信记录中同时有发送和接收短信的用户数|interactive_user_cnt()|-0.001900|
|interactive_call_user_ratio|通话记录中同时有拨打和接听的用户占比|interactive_user_cnt()|-0.450867|
|interactive_sms_user_ratio|短信记录中同时有发送和接收短信的用户占比|interactive_user_cnt()|0.029235|
|2020年7月6日新加工特征| | | |
|duration_days_min|与用户的最小通话持续天数|same_user_call_time_last()|-0.033254|
|duration_days_max|与用户的最大通话持续天数|same_user_call_time_last()|-0.363072|
|duration_days_mean|与用户的平均通话持续天数|same_user_call_time_last()|-0.337290|
|duration_days_median|与用户的通话持续天数中位数|same_user_call_time_last()|-0.139230|
|duration_days_std|与用户的通话持续天数方差|same_user_call_time_last()|-0.431158|
|user_duration_min|与同一用户通话总时长的最小时长|same_user_total_duration()|-0.026407|
|user_duration_max|与同一用户通话总时长的最大时长|same_user_total_duration()|-0.007095|
|user_duration_mean|与同一用户通话总时长的平均时长|same_user_total_duration()|-0.066084|
|user_duration_median|与同一用户通话总时长的中位数|same_user_total_duration()|-0.087978|
|user_duration_std|与同一用户通话总时长的方差|same_user_total_duration()|-0.043611|
|2020年7月7日新加工特征| | | |
|voc_cnt_class|用户通话记录条数等频分箱结果|get_split_box_label(data, "voc_cnt", 4)|IV:1.94|
|voc_user_mean_cnt_class|与同一个人通话的平均次数分箱结果|get_split_box_label(data, "", 4)|IV:2.96|
|voc_user_cnt_class|通话记录中的人数分箱结果|get_split_box_label(data, "", 4)|IV:2.25|
|call_type_1_cnt_class|主呼次数分箱结果|get_split_box_label(data, "", 4)|IV:2.03|
|call_type_2_cnt_class|被呼次数分箱结果|get_split_box_label(data, "", 5)|IV:1.32|
|sms_cnt_class|短信记录分箱结果|get_split_box_label(data, "", 4)|IV:1.80|
|sms_type_2_cnt_class|接收短信记录分箱结果|get_split_box_label(data, "", 4)|IV:1.80|
|flow_class|app流量总和分箱结果|get_split_box_label(data, "", 6)|IV:0.88|
|active_days_class|活跃天数分箱结果|get_split_box_label(data, "", 4)|IV:2.23|
|call_high_risk_opposite_cnt|通话记录中含有的高危号码数目|call_high_risk_opposite(data, "", 4)|0.342|
|call_high_risk_opposite_label|通话记录中含有的高危号码|call_high_risk_opposite(data, "", 4)|0.611|
|sms_high_risk_opposite_label|短信记录中含有的高危号码|sms_high_risk_opposite(data, "", 4)|0.611|
|sms_high_risk_opposite_cnt|短信记录中含有的高危号码数目|sms_high_risk_opposite(data, "", 4)|0.131|
|2020年7月8日新加工特征| | | |
|call_user_cnt|通话记录中的用户数|call_user_cnt()|0.145|
|initiative_call_user_cnt|主呼通话记录中的用户数|initiative_call_user_cnt()|0.165|
|initiative_call_user_ratio|主呼通话中用户数量占通话记录中用户数量的比例|initiative_call_user_ratio()|-0.410|
|passive_call_user_cnt|被呼通话记录中的用户数|passive_call_user_cnt()|-0.186|
|passive_call_user_ratio|被呼通话中用户数量占通话记录中用户数量的比例|passive_call_user_ratio()|-0.558|
|initiative_passive_user_ratio|主呼通话记录中的人数除以被呼通话记录中的人数|initiative_passive_user_ratio()|-0.08|
|turn_call_user_cnt|呼转通话记录中的用户数|turn_call_user_cnt()|-0.024|
|turn_call_user_ratio|呼转通话中用户数量占通话记录中用户数量的比例|turn_call_user_ratio()|-0.027|
|sms_user_cnt|短信记录中的用户数|sms_user_cnt()|0.024|
|initiative_sms_user_cnt|发送短信记录中用户数量|initiative_sms_user_cnt()|0.041|
|initiative_sms_user_ratio|发送短信记录中用户数量占短信记录中用户数量的比例|initiative_sms_user_ratio()|0.071|
|passive_sms_user_cnt|接收短信记录中用户数量|passive_sms_user_cnt()|0.148|
|passive_sms_user_ratio|接收短信记录中用户数量占短信记录中用户数量的比例|passive_sms_user_ratio()|0.131|
|2020年7月10日新加工特征| | | |
|user_imei_user_cnt|用户关联的imei关联的用户数总和|user_imei_user_cnt()|-0.181|

### 归属地诈骗电话占比(城市级)(search_high_risk_city_areas)

|城市|诈骗电话数目|总电话数目|诈骗电话占比|
|:--|:--|:--|:--|
|成都|928|3281|0.282841|
|乐山|103|488|0.211066|
|广安|38|189|0.201058|
|达州|77|383|0.201044|
|宜宾|73|369|0.197832|
|德阳|149|759|0.196311|
|泸州|58|317|0.182965|
|遂宁|88|484|0.181818|
|巴中|31|176|0.176136|
|内江|75|431|0.174014|
|南充|89|515|0.172816|
|绵阳|125|732|0.170765|
|广元|50|301|0.166113|
|资阳|99|640|0.154688|
|眉山|100|654|0.152905|
|阿坝|26|193|0.134715|
|凉山|40|308|0.12987|
|自贡|51|424|0.120283|
|攀枝花|19|165|0.115152|
|雅安|46|425|0.108235|
|甘孜|11|102|0.107843|

### 归属地诈骗电话占比(区县级)(search_high_risk_county_areas)
明细文件地址：high_risk_area_county.xlsx

|区县|诈骗电话数目|总电话数目|诈骗电话占比|
|:--|:--|:--|:--|
|得荣县|2|3|0.667|
|金阳县|3|7|0.429|

### 高危APP列表(app_app_name)
明细文件地址：high_risk_app.xlsx