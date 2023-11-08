from en_galileo_sdk.utility.login import login
import pytest
from utils.encrypt import decrypt

@pytest.fixture(scope="session",autouse=True)
def get_token():
    token = login(username='Testplatform', password=decrypt('gAAAAABlS1vLzAxn8YVhPDOndyXKmId83nfhIqdLAyxsKBGzswIZxE9LzoO-ZdWZoJyauKHNeDjMy0YulbddSq5EBmj1VR84qA==','a9NIqbxL7YkaKqmhqqzz_15KnjDwLeF02gDIaPqnnzg='),account_type=1)
    return token