#!/usr/bin/env python
# coding: utf-8

# # EACE仿真数据获取
# 
# **访问托管区内部 EACE系统仿真数据**
# 
#  -风机查询
#  
#  -统计数据
#  
#  -时序数据
#  
#  -疲劳载荷


import pprint
import pandas as pd
from en_galileo_sdk.data_access.ace.ace_connector import AceOnlineConnector
from en_galileo_sdk.data_access.ace.ace_analysis_data import AceAnalysisData
import allure

@allure.feature("EACE仿真数据获取Demo")
def test_ace_dataanalysis():
    with allure.step("断言获取连接不为None"):
        ace_conn = AceOnlineConnector()
        assert ace_conn is not None
    
    with allure.step("断言获取到的风机信息字典不为空"):
        turbine_info = ace_conn.get_turbines_info()
        assert bool(turbine_info)
        
    with allure.step("断言建立分析后能获取统计数据"):
        ace_obj = AceAnalysisData(ace_conn, '2DP_117_EN50_EN156A_140HH_IEC_085C_50Hz_BinHaiPrototype', 'V1', 'Sim5')
        stat_channels = [
            {'stat_type': 'mean', 'cmptId': 'Blade 1', 'frameId': 'Blade root axes', 'varId': 'Mx', 'sectId': 'root', 'unitId': 'N-m'},
            {'stat_type': 'mean', 'cmptId': 'Blade 1', 'frameId': 'Blade root axes', 'varId': 'My', 'sectId': 'root', 'unitId': 'N-m'},
            {'stat_type': 'mean', 'cmptId': 'Blade 1', 'frameId': 'Blade root axes', 'varId': 'Mxy', 'sectId': 'root', 'unitId': 'N-m'}
        ]
        stat_data = ace_obj.get_statistics_data(stat_channels, dlc = ['1.3'])
        df1 = pd.DataFrame(stat_data)
        assert df1.shape[0] ==572, "返回的数据个数应该等于572"
        assert df1.shape[1]  == 5,"列数应该有5列"
        assert set(["dlc","case_name","mean_Blade 1_Blade root axes_Mx_root_N-m",	"mean_Blade 1_Blade root axes_My_root_N-m",	"mean_Blade 1_Blade root axes_Mxy_root_N-m"]).issubset(df.columns)
    
    with allure.step("断言获取时序数据"):
        ts_data = ace_obj.get_timeseries_data(stat_channels, dlc = ['1.3'])
        df2 = pd.DataFrame(ts_data)
        top5 = df2.head()
        assert top5.shape[0] == 5, "返回的数据个数应该等于5"
        assert top5.shape[1] == 5,"列数应该有5列"
        assert set(["dlc","case_name","mean_Blade 1_Blade root axes_Mx_root_N-m",	"mean_Blade 1_Blade root axes_My_root_N-m",	"mean_Blade 1_Blade root axes_Mxy_root_N-m"]).issubset(df.columns)

