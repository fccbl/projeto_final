import pytest
import requests
import random

@pytest.fixture(scope="session") 
def base_url(): 
  """Provides the base URL for the API.""" 
  return "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def token(base_url):
    response = requests.post(f"{base_url}/auth/login",
        json={"email": "projeto@example.com","password": "Senha123!"})
    
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def new_user_token(base_url):
    """Cria um novo usuário e retorna seu token."""

    email = f"user_b_{random.randint(10000, 99999)}@example.com"
    password = "Senha123!"
    username = f"userb_{random.randint(10000, 99999)}"

    user_payload = {"email": email,"password": password,"username": username}

    create_user = requests.post(f"{base_url}/auth/register",json=user_payload)
    assert create_user.status_code == 200

    login_payload = {"email": email, "password": password}

    login = requests.post(f"{base_url}/auth/login",json=login_payload)
   
    assert login.status_code == 200

    return login.json()["access_token"]

   