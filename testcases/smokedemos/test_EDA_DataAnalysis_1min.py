#!/usr/bin/env python
# coding: utf-8

# # 获取DigitalTwin-1min的通道数据

# ## 1. 导入包

import pandas as pd
from en_galileo_sdk.data_access.eda.eda_connector import  EdaConnector
from en_galileo_sdk.data_access.eda.eda_analysis_data import EdaAnalysisData
import allure

def test_EDA_DataAnaylysis_1min():
    '''1min 分析demo
    
    '''
    eda_conn = EdaConnector()


    # ### 2.1 获取风场信息
    with allure.step("断言能够获取到风场信息"):
        wind_farm_list=eda_conn.get_wind_farm_list()
        wind_farm_df = pd.DataFrame(wind_farm_list)
        assert wind_farm_df[wind_farm_df.wind_farm_name.str.contains('打鼓')].iloc[0].at['abbreviation']=='JXDG'


    # ### 2.2 获取风机详情
    with allure.step("断言能够获取到风机信息"):
        wind_turbine_detail=eda_conn.get_wind_turbine_list(['JXDG'])['JXDG']
        assert pd.DataFrame(wind_turbine_detail).iloc[0].at['assets_wind_turbine_id']=='CN-33/07-B-001'


    # ### 2.3 获取DigitalTwin-1min通道信息
    with allure.step("断言能够获取DigitalTwin-1min通道信息"):
        channel_list=eda_conn.get_channel_list(name='%PTH%1min%')
        assert pd.DataFrame(channel_list).iloc[0].at['original_name'] == 'PTH_Pitch1Ave_1min'


    # ## 3. 获取DigitalTwin数据
    # ### 3.1 定义参数
    with allure.step("断言能够获取DigitalTwin数据"):   
        wind_farm_turbine_dict = {'CN-33/07': ['CN-33/07-B-001']}
        start_time = "2021-06-01 00:00:00"
        end_time = "2021-06-10 00:00:00"
        channel_list=['PTH_Pitch1Ave_1min','PTH_Pitch1Max_1min', 'PTH_Pitch1Min_1min', 'PTH_Pitch1Std_1min']
        eda_obj = EdaAnalysisData(eda_conn, wind_farm_turbine_dict, start_time, end_time)
        dt_statistics_data = eda_obj.get_dt_1min_data(channel_list)
        df = pd.DataFrame(dt_statistics_data['CN-33/07']['CN-33/07-B-001'])
        assert df.shape[0] == 9991,"数据应有9991行"
        assert df.shape[1] == 4,"应有4列"


