import os
import pandas as pd
import glob

data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),"testdata")
download_dir = "D:\\autotestdata\\sdk-download-files\\"


def read_csv_as_dataframe(csv_name):
    df_expect = pd.read_csv(os.path.join(data_dir,csv_name))
    return df_expect

def check_file_exists(file_name):
    files = glob.glob(os.path.join(download_dir,file_name))
    return len(files)>0