import requests 
import logging

def test_add_product_to_wishlist(base_url, token):
# Scenario 21: Successfully Add a Product to a Wishlist

    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "Product": "New Gadget",
        "Price": "99.99",
        "Zipcode": "12345678",
        "delivery_estimate": "3 days",
        "shipping_fee": "5.00"
    }

    logging.info("📦 Enviando requisição para adicionar produto à wishlist 6")

    response = requests.post(f"{base_url}/wishlists/6/products",json=product_payload,headers=headers)

    assert response.status_code == 200
    logging.info("✅ Produto adicionado com sucesso (status 200)")

    data = response.json()
    assert "id" in data
    assert data["wishlist_id"] == 6
    assert data["is_purchased"] is False

    logging.info(f" Detalhes do produto criado: "f"ID={data['id']}, Nome={data['Product']}, Wishlist={data['wishlist_id']}")

def test_add_product_to_nonexistent_wishlist(base_url, token):
# Scenario 22: Add a Product to a Non-Existent 

    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "Product": "Smartwatch",
        "Price": "499.90",
        "Zipcode": "12345678",
        "delivery_estimate": "4 days",
        "shipping_fee": "5.00"
    }

    logging.info("Tentando adicionar produto a uma wishlist com ID=999")

    response = requests.post(f"{base_url}/wishlists/999/products",json=product_payload,headers=headers)

    assert response.status_code == 404
    logging.info("Requisição retornou 404 - Wishlist não encontrada")

    message = response.text.lower()
    assert "wishlist not found" in message
    logging.info("Mensagem de erro confirma que a wishlist não existe")

def test_add_product_to_other_user_wishlist(base_url):
# Scenario 23: Ensure a user cannot add a product to a wishlist they do not own

    register_payload = {
        "email": "userb2@example.com",
        "password": "Senha1234!",
        "username": "userb2"
    }
    register_response = requests.post(f"{base_url}/auth/register", json=register_payload)
    assert register_response.status_code == 200
    logging.info("Usuário registrado com sucesso (status 200)")


    
    login_payload = {"email": "userb2@example.com", "password": "Senha1234!"}
    login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert login_response.status_code == 200
    logging.info("Login realizado com sucesso (User B).")

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

 
    product_payload = {
        "Product": "Headset Gamer",
        "Price": "15.99",
        "Zipcode": "90210",
        "delivery_estimate": "5 days",
        "shipping_fee": "2.00"
    }

    response = requests.post(f"{base_url}/wishlists/1/products", json=product_payload, headers=headers)
    logging.info("Tentando adicionar produto a uma wishlist pertencente a outro usuário.")

    assert response.status_code == 404
    logging.info(" Status 404 — wishlist não encontrada para o usuário autenticado.")

def test_add_product_with_incomplete_data(base_url,token):
# Scenario 24: Add a Product with Incomplete Data

      headers = {"Authorization": f"Bearer {token}"}

      incomplete_payload = {"Price": "10.00"}

      logging.info("Tentando adicionar produto com campos incompletos")

      response = requests.post(f"{base_url}/wishlists/1/products",json=incomplete_payload,headers=headers)

      assert response.status_code == 422
      logging.info("Status 422 — produto não foi adicionado por falta de dados obrigatórios.")

      message = response.text.lower()
      assert "missing" in message
      logging.info("Mensagem de erro confirma que os campos obrigatórios estão ausentes.")