import requests
import os
from dotenv import load_dotenv


# Carrega variáveis do .env
load_dotenv()

API_URL = os.getenv("API_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def get_token():
    """Faz login e retorna o token de acesso"""
    url = f"{API_URL}/auth/login"
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Erro ao fazer login: {response.text}")


def get_wishlist_products():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_URL}/wishlists/1/products", headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Erro ao buscar produtos: {resp.text}")
    produtos = resp.json()
    
    return produtos

