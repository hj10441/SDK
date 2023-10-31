from en_galileo_sdk.data_access.eda.eda_connector import EdaConnector
from en_galileo_sdk.data_access.eda.eda_analysis_data import EdaAnalysisData
from en_galileo_sdk.utility.login import login
import pytest

@pytest.fixture(scope="session",autouse=True)
def get_token():
    token = login(username='Testplatform', password='pqxY89lw*',account_type=1)
    return token