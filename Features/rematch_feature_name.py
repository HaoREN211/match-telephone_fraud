# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/25 9:50
# IDE：PyCharm

class ColumnName(object):

    # 通话记录中的通话类型
    voc_type = {0: "通话记录", 1: "主动拨打电话记录", 2: "被动接听电话记录", 3: "呼转电话记录"}
    sms_type = {0: "短信记录", 1: "主动发送短信记录", 2: "被动接收短信记录"}

    prefix_voc_type = {0: "", 1: "initiative_", 2: "passive_", 3: "turn_"}

    def __init__(self):

        # 通话记录中imei的数量
        self.columns_voc_imei_cnt = {}

        # 通话时长
        self.columns_voc_call_dur = {}

        # 通话活跃天数
        self.columns_voc_active_days = {}

        # 短信活跃天数
        self.columns_sms_active_days = {}

        for i in range(4):
            self.columns_voc_imei_cnt[i] = self.prefix_voc_type[i]+"voc_imei_cnt"
            self.columns_voc_call_dur[i] = self.prefix_voc_type[i]+"voc_dur"
            self.columns_voc_active_days[i] = self.prefix_voc_type[i] + "voc_active_days"
            self.columns_sms_active_days[i] = self.prefix_voc_type[i] + "sms_active_days"
