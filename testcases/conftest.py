from en_galileo_sdk.data_access.eda.eda_connector import EdaConnector
from en_galileo_sdk.data_access.eda.eda_analysis_data import EdaAnalysisData
from en_galileo_sdk.utility.login import login
import pytest

@pytest.fixture(scope="session",autouse=True)
def login():
    token = login(username='xxx', password='xxxxxx',account_type=1)
    eda_conn = EdaConnector(token=token)