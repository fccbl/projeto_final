import requests
import logging

def test_create_wishlist_successfully(base_url):
#Scenario 14: Successfully Create a Wishlist

    login_payload = {"email": "projeto@example.com", "password": "Senha123!"}
    login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert login_response.status_code == 200
    logging.info("Login realizado com sucesso (status 200)")
    token = login_response.json()["access_token"]
    logging.info(" Token obtido")

    headers = {"Authorization": f"Bearer {token}"}

    wishlist_payload = {"name": "My Tech Gadgets 3"}
    response = requests.post(f"{base_url}/wishlists", json=wishlist_payload, headers=headers)
    logging.info("Criando uma nova wishlist")

    assert response.status_code == 200
    logging.info("Wishlist criada com sucesso (status 200)")

    data = response.json()
    assert "id" in data
    assert data["name"] == "My Tech Gadgets 3"
    assert "owner_id" in data
    logging.info(f"✅ Wishlist criada com sucesso: id={data['id']}, name={data['name']}, owner_id={data['owner_id']}")

def test_prevent_duplicate_wishlist_creation(base_url):
# Scenario 15: Prevent Duplicate Wishlist Creation

    login_payload = {"email": "projeto@example.com", "password": "Senha123!"}
    login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert login_response.status_code == 200
    logging.info("Login realizado com sucesso (status 200)")

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"name": "Travel Plans 321"}
    first_response = requests.post(f"{base_url}/wishlists", json=payload, headers=headers)
    assert first_response.status_code == 200

    first_data = first_response.json()
    logging.info(f"Primeira wishlist criada: id={first_data['id']}, name={first_data['name']}")

    second_response = requests.post(f"{base_url}/wishlists", json=payload, headers=headers)
    logging.info("Tentativa de criar wishlist com nome duplicado")

    assert second_response.status_code == 409
    logging.info("API retornou 409 para nome de wishlist duplicado")

    response_text = second_response.text.lower()
    assert "already exists" in response_text 
    logging.info(" Mensagem de erro indica que o nome da wishlist já existe")

    assert "id" not in second_response.text
    logging.info("Nenhum novo ID na resposta")
    
def test_create_wishlist_unauthenticated(base_url):
# Scenario 16: Unauthenticated user cannot create wishlist

    payload = {"name": "Test_Wishlist"}

    response = requests.post(f"{base_url}/wishlists", json=payload)
    logging.info("Tentativa de criar wishlist sem autenticação")

    assert response.status_code == 401
    logging.info("API retornou 401 para requisição sem autenticação")

    response_text = response.text.lower()
    assert "not authenticated" in response_text
    logging.info("Mensagem de erro indica que o usuário não está autenticado")
   
def test_create_wishlist_with_invalid_data(base_url):
# Scenario 17: Create a Wishlist with Invalid Data

    login_payload = {"email": "projeto@example.com", "password": "Senha123!"}
    login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert login_response.status_code == 200
    logging.info("Login realizado com sucesso (status 200)")

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    invalid_payload = {}
    response = requests.post(f"{base_url}/wishlists", json=invalid_payload, headers=headers)
    logging.info("Tentativa de criar wishlist sem nome")

    assert response.status_code == 422
    logging.info("API retornou 422 para requisição inválida")

    response_text = response.text.lower()
    assert "missing name" in response_text 
    logging.info("Mensagem de erro indica que o campo 'name' é obrigatório")
    
