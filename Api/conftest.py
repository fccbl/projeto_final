import pytest

@pytest.fixture(scope="session") 
def base_url(): 
  """Provides the base URL for the API.""" 
  return "http://127.0.0.1:8000"