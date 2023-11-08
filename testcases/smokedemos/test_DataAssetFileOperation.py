#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from en_galileo_sdk.data_access.center.data_asset_analysis_data import DataAssetAnalysisData
from en_galileo_sdk.data_access.center.data_asset_connector import DataAssetConnector
import allure
import utils.file_operation as fp
import datetime

@allure.feature("数据资产文件操作Demo")
def test_ace_dataanalysis():
    '''数据资产文件操作Demo
    注意：本用例不验证上传和解冻
    '''
    with allure.step("断言获取连接不为None"):        
        con = DataAssetConnector()
        assert con is not None



    # 设置字体样式和正常显示字符
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False


    with allure.step("断言能获取资产数据"):
        obj = DataAssetAnalysisData(con)   
        data_asset_objects = con.get_data_asset_objects()
        df = pd.DataFrame(data_asset_objects)
        assert df.shape[0] > 90, "返回的资产数据个数应该大于90"
        assert df.shape[1]  == 7,"列数应该有7列"


    with allure.step("断言能够获取数据资产下的数据连接（S3目录）"):
        connections = con.list_file_connections("SystemOperationData_ODS_EDASystemLog")
        df = pd.DataFrame(connections)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"
        
        path = connections[0]["includePath"]
        assert path == 's3://engineeringbigdata/ODS/SystemOperationData/SDKLog/'
        
        paths = con.list_paths("SystemOperationData_ODS_EDASystemLog",include_path=connections[0]["includePath"])
        pd.DataFrame(paths)
        assert df.shape[0] > 0, "返回的数据个数应该大于0"

    with allure.step("断言文件下载是成功的"):
        file_paths = con.list_paths("SystemOperationData_ODS_EDASystemLog",include_path=paths[0]["path"])
        assert con.download_files("SystemOperationData_ODS_EDASystemLog",file_paths=[file_paths[0]["path"]],target_dir="D:\\autotest\\sdk-download-files\\")
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y%m%d_%H%M")
        assert fp.check_file_exists(f"BatchDownload_{formatted_time}*.zip")
        




