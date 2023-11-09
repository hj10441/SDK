#!/usr/bin/env python
# coding: utf-8

# # Digital Twin叶根弯矩极限值分布统计

# ## 1. 定义数据集

# In[1]:


# coding=utf-8
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from en_galileo_sdk.data_access.eda.eda_connector import EdaConnector
from en_galileo_sdk.data_access.eda.eda_analysis_data import EdaAnalysisData
import allure


@allure.feature("数据资产文件操作Demo")
def test_eda_bladerootanalysis():
    '''Digital Twin叶根弯矩极限值分布统计 Demo
    注意：本用例不验证画图功能
    '''
    with allure.step("断言获取连接不为None"):
        dt_conn = EdaConnector()
        assert dt_conn is not None


    with allure.step("断言能正常获取数据"):
        # 定义数据集
        wind_farm_turbine_dict = {
            "CN-81/05": ["CN-81/05-B-001", "CN-81/05-B-006"]}
        start_time = "2020-03-01 00:00:00"
        end_time = "2020-08-30 01:00:00"
        # ## 2. 定义筛选条件
        blade_part_id = "3016505"  # SM121D物料号，加入数仓维度表中后只需指定型号SM121D
        value_filter = '`Stat_BR2FlapBM_Max`<20000.0'
        dim_filter = "`blade_part_id` in ('%s')" % blade_part_id
        stat_channel_list = ["Stat_BR2EdgeBM_Max", "Stat_BR2FlapBM_Max"]

        dt_obj = EdaAnalysisData(dt_conn, wind_farm_turbine_dict, start_time, end_time)
        data = dt_obj.query_dt_data(stat_channel_list, dim_filter=dim_filter, value_filter=value_filter, group_name='wtg_alias', agg_func='max')
        dt = pd.DataFrame(data)
        assert dt.shape[0] > 1, "获取的数据应该大于1条"
        assert dt.shape[1] == 4, "列数应该有4列"




