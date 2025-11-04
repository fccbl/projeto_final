import requests
import logging

def test_register_new_user(base_url):
#Scenario 8: Successful User Registration

     payload = {"email": "fabiana_cesar_projeto@example.com","password": "password5234","username": "fafa_projeto"}
     response = requests.post(f"{base_url}/auth/register", json= payload)
     assert response.status_code == 200
     logging.info("Usuário registrado com sucesso (status 200)")
    
     data = response.json()

     assert "email" in data, "Campo 'email' não encontrado na resposta"
     assert data["email"] == payload["email"], "O e-mail retornado não corresponde ao enviado"
     assert "id" in data, "Campo 'id' não encontrado na resposta"

     assert "password" not in data, "Campo 'password' não deveria estar presente na resposta"

     logging.info(f"Dados retornados: {data}")

def test_register_existing_email(base_url):
#Scenario 9: Registration with an Existing Email   

   payload = {"email": "usertest@example.com", "password": "password345", "username": "user"}

   first_response = requests.post(f"{base_url}/auth/register", json=payload)
   assert first_response.status_code == 200
   logging.info("Usuário registrado com sucesso (status 200)")
    
   second_response = requests.post(f"{base_url}/auth/register", json=payload)
   logging.info(f"Tentativa de registro com e-mail já existente")
    
   assert second_response.status_code == 400
   logging.info("API retornou status 400 conforme esperado")

   assert "email already registered" in second_response.text.lower()
   logging.info("✅ Mensagem de erro indica que o e-mail já está registrado")

def test_register_with_invalid_data(base_url):
#Scenario 10: Registration with Invalid Data   

    payload = { "email": "not-an-email", "password": "password123", "username": "user_invalid_email"}

    response_invalid_email = requests.post(f"{base_url}/auth/register", json= payload)
    logging.info("Tentativa de registro com e-mail inválido")

    assert response_invalid_email.status_code == 422
    logging.info("API retornou 422 para e-mail inválido")

    assert "invalid email format" in response_invalid_email.text.lower()
    logging.info("✅ Mensagem de erro indica e-mail inválido")

    missing_password_payload = { "email": "user_without_password@example.com","username": "user_no_password"}

    response_missing_password = requests.post(f"{base_url}/auth/register", json=missing_password_payload)
    logging.info("Tentativa de registro sem senha")

    assert response_missing_password.status_code == 422
    logging.info("API retornou 422 para requisição sem senha")

    assert "missing data" in response_missing_password.text.lower()
    logging.info("✅ Mensagem de erro indica que o campo de senha é obrigatório")