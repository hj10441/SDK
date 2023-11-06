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
from en_galileo_sdk.data_access.center.data_asset_analysis_data import DataAssetAnalysisData
from en_galileo_sdk.data_access.center.data_asset_connector import DataAssetConnector
import pytest
import allure
from logger.allure_log_handler import logger

@pytest.fixture(scope="module")
def get_data_asset_connector(get_token):
    yield DataAssetConnector(get_token)

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
        logger.warning(df)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"
        assert df.shape[1] == 7, "列数应该有7列"
        assert set(['name','code','description','owner','domain','layer','application']).issubset(df.columns)
    
    @allure.story("数据模型列表")
    def test_get_tables(self,get_data_asset_connector):
        '''查询数据资产的数据模型列表,检查点：
        1. 表名包含领域+Layer+Application+资产名
        2. 返回的数据个数大于0
        '''
        tables = get_data_asset_connector.get_tables(data_asset_code='WindWorkOrder')
        df = pd.DataFrame(tables)
        logger.warning(df)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"
        assert df.shape[1] > 0,  "返回的列数应该大于0"
        for idx,row in df.iterrows() :
            assert "windturbineoperationdata_prod_galileo_windworkorder" in row['name']