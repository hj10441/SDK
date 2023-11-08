#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file : test_data_asset_analysis_data.py
@comment: 测试数据资产获取API
@date : 2023/10/19 14:21:54
@author : xiu.jiang
@version : 1.0
'''
import pandas as pd
from en_galileo_sdk.data_access.center.data_asset_connector import DataAssetConnector
from en_galileo_sdk.data_access.center.data_asset_analysis_data import DataAssetAnalysisData
from en_galileo_sdk.utility.exceptions import HttpResponseError
import pytest
import allure
from logger.allure_log_handler import logger

@pytest.fixture(scope="module")
def get_data_asset_connector(get_token):
    yield DataAssetConnector(get_token)

data_asset_code = "WindWorkOrder"

@allure.feature("测试数据资产获取API")
class TestDataAssetAnalysisData: 
    
    @allure.story("数据资产列表")
    def test_get_data_asset_objects(self,get_data_asset_connector):
        '''查询数据资产列表,检查点：
        1. 列表是否7列，列名是否正确
        2. 返回的数据个数大于0
        '''
        data_asset_objects = get_data_asset_connector.get_data_asset_objects()
        df = pd.DataFrame(data_asset_objects)
        #logger.warning(df)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"
        assert df.shape[1] == 7, "列数应该有7列"
        assert set(['name','code','description','owner','domain','layer','application']).issubset(df.columns)
    
    @allure.story("数据资产的表")
    def test_get_tables(self,get_data_asset_connector):
        '''查询数据资产的表,检查点：
        1. 表名包含领域+Layer+Application+资产名
        2. 返回的数据个数大于0
        '''
        tables = get_data_asset_connector.get_tables(data_asset_code=data_asset_code )
        df = pd.DataFrame(tables)
        #logger.warning(df)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"
        assert df.shape[1] > 0,  "返回的列数应该大于0"
        for idx,row in df.iterrows() :
            assert "windturbineoperationdata_prod_galileo_windworkorder" in row['name']
    
    @allure.story("数据资产的模型")
    def test_get_models(self,get_data_asset_connector):
        '''查询数据资产的数据模型,检查点：
        1. 列表是否2列，列名是否正确
        2. 返回的数据个数大于0
        '''
        tables = get_data_asset_connector.get_tables(data_asset_code=data_asset_code)
        df = pd.DataFrame(tables)
        assert df.shape[0] > 0, "返回的模型个数应该大于0"
        assert df.shape[1]  == 2,"列数应该有2列"
        assert set(["name","description"]).issubset(df.columns)
    
    @allure.story("查询表/模型的元数据信息")
    def test_get_metadata(self,get_data_asset_connector):
        ''' 查询元数据信息,检查点:
        1.表和模型的元数据信息都可以查看
        '''
        meta = get_data_asset_connector.get_metadata(data_asset_code=data_asset_code,
                        data_type='table',
                        name='windturbineoperationdata_prod_galileo_windworkorder_workorder')
        df = pd.DataFrame(meta)
        assert df.shape[0] > 0, "返回的元数据个数应该大于0"
        assert df.shape[1]  == 3,"列数应该有3列"
        assert set(["name","type","comment"]).issubset(df.columns)
        
        meta = get_data_asset_connector.get_metadata(data_asset_code=data_asset_code,
                        data_type='model',
                        name='windturbineoperationdata_prod_galileo_windworkorder_workcategory') 
        assert df.shape[0] > 0, "返回的元数据个数应该大于0"
        assert df.shape[1]  == 3,"列数应该有3列"
        assert set(["name","type","comment"]).issubset(df.columns)

    
    @allure.story("查询资产数据-Gaia测试平台数据")
    def test_get_data_v2(self,get_data_asset_connector):
        ''' 查询资产数据信息,检查点:
        1. 是否有返回值
        2. 是否根据过滤条件进行了正确筛选
        3. 排序是否起作用
        4. 过滤字段是否区分大小写
        5. 检查limit是否生效
        '''
        obj = DataAssetAnalysisData(get_data_asset_connector)
        data_result = obj.get_data_v2(
            name='wind_prod_testplatform_gaia_data_testresult',
            condition={
                "filter[create_time][GT]": '2023-11-02 13:54:42.0',
                "filter[create_time][LE]": '2023-11-02 16:53:33.0',
                "fields": "name,progress,result,time_cost",
                "sort": "-progress,time_cost"
            },
            limit=8
        )
        df = pd.DataFrame(data_result)
        df_expect = pd.read_csv('../testdata/gaia_test_result.csv')
        assert df.equals(df_expect) 
        
        
        
    @allure.story("没有数据资产权限时")
    def test_permission_denied(self,get_data_asset_connector):
        '''检查点：
        1. 没有数据资产权限时，可以查表/模型 列表，但是查不了数据
        '''
        obj = DataAssetAnalysisData(get_data_asset_connector)
        with pytest.raises(HttpResponseError) as exc_info:
            obj.get_data_v2(
            name='windturbineoperationdata_prod_galileo_perspect_alarm_cards',
            condition={
            },
            limit=10)
            assert exc_info.value == '无访问权限.'
    
    @allure.story('测试翻页功能')
    @pytest.mark.skip()
    def test_next_marker(self,get_data_asset_connector):
        # TODO v2要到3.0.5
        connections = get_data_asset_connector.list_file_connections("lmt")

        paths = get_data_asset_connector.list_paths_v2("lmt",include_path=connections[0]["includePath"])


        paths1 = get_data_asset_connector.list_paths_2("lmt",include_path=connections[0]["includePath"],next_marker='s3://lmt/netoff/data/test01.txt')

        pd.DataFrame(paths1)
        
        
        assert 1 == 1 