import os
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),"testdata")

def read_csv_as_dataframe(csv_name):
    df_expect = pd.read_csv(os.path.join(data_dir,csv_name))
    return df_expect