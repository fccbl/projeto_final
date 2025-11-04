import requests 
import logging

# def test_add_product_to_wishlist(base_url):
# # Scenario 21: Successfully Add a Product to a Wishlist

#     login_payload = {"email": "projeto@example.com", "password": "Senha123!"}
#     login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
#     assert login_response.status_code == 200
#     logging.info("✅ Login realizado com sucesso")

   
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}

    
#     product_payload = {
#         "Product": "New Gadget",
#         "Price": "99.99",
#         "Zipcode": "12345678",
#         "delivery_estimate": "3 days",
#         "shipping_fee": "5.00"
#     }

#     response = requests.post(f"{base_url}/wishlists/6/products", json=product_payload, headers=headers)
#     logging.info("📦 Enviando requisição para adicionar produto à wishlist 6")

#     assert response.status_code == 200
#     logging.info("✅ Produto adicionado com sucesso (status 200)")

#     data = response.json()
#     assert "id" in data
#     assert data["wishlist_id"] == 6
#     assert data["is_purchased"] is False
#     logging.info(f" Detalhes do produto criado: ID={data['id']}, Nome={data['Product']}, Wishlist={data['wishlist_id']}")

def test_add_product_to_nonexistent_wishlist(base_url):
# Scenario 22: Add a Product to a Non-Existent Wishlist

    login_payload = {"email": "projeto@example.com", "password": "Senha123!"}
    login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
    assert login_response.status_code == 200
    logging.info(" Login realizado com sucesso")

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Dados do produto
    product_payload = {
        "Product": "Smartwatch ",
        "Price": "499.90",
        "Zipcode": "12345678",
        "delivery_estimate": "4 days",
        "shipping_fee": "5.00"
    }

    response = requests.post(f"{base_url}/wishlists/999/products", json=product_payload, headers=headers)
    logging.info("Tentando adicionar produto a uma wishlist com ID=999")

    assert response.status_code == 404
    logging.info("Requisição retornou 404 - Wishlist não encontrada")

    message = response.text.lower()
    assert "wishlist not found" in message
    logging.info("Mensagem de erro confirma que a wishlist não existe")

