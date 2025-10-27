import pytest
import csv
from selenium import webdriver

@pytest.fixture
def driver():
    """
    Cria uma instância do Chrome, maximiza a janela e fecha ao final do teste.
    """
    driver_instance = webdriver.Chrome()
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture
def base_url_americanas():
  
  return "https://www.americanas.com.br"

@pytest.fixture
def temp_mail_url():
    return "https://temp-mail.io/"


def load_csv_test_cases(path):
    """Reads a CSV file and returns a list of dictionaries."""
    cases = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cases.append(row)
    return cases
