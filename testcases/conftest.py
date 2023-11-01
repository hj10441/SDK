from en_galileo_sdk.utility.login import login
import pytest

@pytest.fixture(scope="session",autouse=True)
def get_token():
    token = login(username='Testplatform', password='pqxY89lw*',account_type=1)
    return token