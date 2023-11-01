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

@pytest.fixture(scope="module")
def get_data_asset_connector(get_token):
    yield DataAssetConnector(get_token)

class TestDataAssetAnalysisData:

    def test_get_data_asset_objects(self,get_data_asset_connector):
        '''查询数据资产列表'''
        data_asset_objects = get_data_asset_connector.get_data_asset_objects()
        df = pd.DataFrame(data_asset_objects)
        assert df.shape[0] == 96
        assert df.shape[1] == 7