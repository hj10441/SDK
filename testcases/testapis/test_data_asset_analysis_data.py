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

class TestDataAssetAnalysisData:
    def setup_class(self,get_token):
        self.con = DataAssetConnector(get_token)

    def test_get_data_asset_objects(self):
        '''查询数据资产列表'''
        data_asset_objects = self.con.get_data_asset_objects()
        assert 1==1