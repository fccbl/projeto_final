import requests
import logging

def test_successful_login(base_url):
#Scenario 11: Successful Login

    payload = {"email": "projeto@example.com","password": "Senha123!"}

    response = requests.post(f"{base_url}/auth/login", json=payload)
    assert response.status_code == 200
    logging.info("Login realizado com sucesso (status 200)")

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    logging.info(" Resposta contém access_token e token_type = bearer")


def test_login_with_incorrect_password(base_url):
#Scenario 12: Login with Incorrect Password
    payload = {"email": "projeto@example.com","password": "senha_errada"}

    response = requests.post(f"{base_url}/auth/login", json=payload)
    assert response.status_code == 401
    logging.info("API retornou 401 para senha incorreta")

    response_text = response.text.lower()
    assert "incorrect email or password" in response_text
    logging.info("Mensagem de erro indica email ou senha incorretos")

def test_login_with_nonexistent_user(base_url):
    # Scenario 13: Login with Non-Existent User

    payload = {"email": "nouser@example.com", "password": "Senha123!"}

    response = requests.post(f"{base_url}/auth/login", json=payload)   
    assert response.status_code == 401
    logging.info("API retornou 401 para usuário inexistente")

    response_text = response.text.lower()
    assert "incorrect email or password" in response_text
    logging.info(" Mensagem de erro indica que o e-mail ou senha estão incorretos")


