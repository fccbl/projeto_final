import requests 
import logging

def test_get_all_wishlists(base_url, token):
# Scenario 18: Successfully Retrieve All Wishlists

     headers = {"Authorization": f"Bearer {token}"}

     logging.info("Requisição enviada para listar todas as wishlists")

     response = requests.get(f"{base_url}/wishlists", headers=headers)

     assert response.status_code == 200
     logging.info("Requisição bem-sucedida (status 200)")

     data = response.json()
     assert isinstance(data, list)
     logging.info(f"Wishlist(s) retornadas: {len(data)}")

def test_get_empty_wishlists(base_url):
#Scenario 19: Retrieve Wishlists When None Exist

    payload = {"email": "sem_lista_0103@example.com","password": "Senha_123!","username": "sem_lista0103"}
    register_response = requests.post(f"{base_url}/auth/register", json=payload)
    assert register_response.status_code == 200
    logging.info("Usuário registrado com sucesso (status 200)")

    data = {"email": "sem_lista0103@example.com","password": "Senha_123!"}
    login_response = requests.post(f"{base_url}/auth/login", json=data)
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/wishlists", headers=headers)

    assert response.status_code == 200
    assert response.json() == []  
    logging.info("Nenhuma wishlist encontrada")

def test_get_wishlists_unauthenticated(base_url):
# Scenario 20: Retrieve Wishlists without Authentication

    response = requests.get(f"{base_url}/wishlists")
    logging.info("Tentativa de listar wishlists sem autenticação")

    assert response.status_code == 401
    logging.info("Usuário não autenticado (status 401)")

    response_text = response.text.lower()
    assert "not authenticated" in response_text
    logging.info("Mensagem de erro indica que o usuário não está autenticado")

