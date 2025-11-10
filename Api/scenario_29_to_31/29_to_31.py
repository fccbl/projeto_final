import requests
import logging

def test_update_product_successfully(base_url, token):
# Scenario 29: Successfully Update a Product

    headers = {"Authorization": f"Bearer {token}"}

    updated_price = "150.00"
    payload = {"Price": updated_price}


    response = requests.put(f"{base_url}/products/1",json=payload,headers=headers)

    assert response.status_code == 200
    logging.info("Produto atualizado com sucesso (200 OK)")

    product = response.json()

    assert isinstance(product, dict)
    assert "id" in product
    assert "Product" in product
    assert "Price" in product
    assert "delivery_estimate" in product
    assert "wishlist_id" in product
    assert "is_purchased" in product

    assert product["Price"] == updated_price
    logging.info("Campo 'Price' atualizado corretamente")

def test_update_nonexistent_product(base_url, token):
#Scenario 30: Update a Product That Doesn't Exist

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"Price": "199.90"}

   
    response = requests.put(f"{base_url}/products/999",json=payload,headers=headers)
  
    assert response.status_code == 404
    logging.info("API retornou 404 ao tentar atualizar um produto inexistente")

def test_prevent_updating_product_not_owned(base_url, new_user_token):
    # Scenario XX: Ensure a user cannot update a product they do not own

    headers = {"Authorization": f"Bearer {new_user_token}"}

    payload = {"Price": "150.00"}

    logging.info("Usuário B tentando atualizar produto que pertence ao usuário A (product_id=1)")

    response = requests.put(
        f"{base_url}/products/1",
        json=payload,
        headers=headers
    )

    assert response.status_code == 404
    logging.info("API retornou 404 — usuário não pode atualizar produto que não pertence a ele")

    message = response.text.lower()
    assert "not found" in message
    logging.info("Mensagem confirma que o produto não foi localizado para o usuário B")
