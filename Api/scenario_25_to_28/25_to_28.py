import requests 
import logging

def test_get_all_products_from_wishlist(base_url, token):
#Scenario 25: Retrieve all products from a specific wishlist

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{base_url}/wishlists/1/products", headers=headers)

    assert response.status_code == 200
    logging.info("API retornou 200 ao buscar produtos da wishlist")

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0
    logging.info("A resposta contém uma lista válida de produtos")

    for p in products:
        assert "id" in p
        assert "Product" in p
        assert "Price" in p
        assert "delivery_estimate" in p
        assert "is_purchased" in p
        assert "wishlist_id" in p and p["wishlist_id"] == 1

    logging.info("Todos os produtos possuem os campos obrigatórios e pertencem à wishlist 1")


def test_filter_products_by_name(base_url, token):
# Scenario 26: Retrieve Products and Filter by Name

    params = {"Product": "iPhone"}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{base_url}/wishlists/1/products",headers=headers,params=params)

    assert response.status_code == 200
    logging.info("API retornou 200 ao filtrar produtos")

    products = response.json()
    assert isinstance(products, list)

    for p in products:
     assert "iPhone".lower() in p["Product"].lower()

    logging.info("Filtro por iPhone validado")

def test_filter_products_by_purchased_status(base_url, token):
    # Scenario 27: Filter products by purchased status

    params = {"is_purchased": "true"}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{base_url}/wishlists/1/products",headers=headers,params=params)

    assert response.status_code == 200
    logging.info("API retornou 200 ao filtrar produtos por status de compra")

    products = response.json()
    assert isinstance(products, list)

    for p in products:
        assert p["is_purchased"] is True

    logging.info("Produtos comprados filtrados corretamente")


def test_cannot_access_other_users_wishlist(base_url, new_user_token):
#Scenario 28: Retrieve Products from Another User's Wishlist

    headers = {"Authorization": f"Bearer {new_user_token}"}

    response = requests.get(f"{base_url}/wishlists/1/products",headers=headers)

    assert response.status_code == 404
    logging.info("API retornou 404 ao tentar acessar wishlist de outro usuário")







