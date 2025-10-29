import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions
import json
from pathlib import Path


@pytest.fixture(scope="function")
def driver():
    """Inicializa o driver Appium e abre o app da Americanas"""
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.b2w.americanas",
        "appium:appActivity": "com.b2w.americanas.MainActivity",
        "appium:noReset": False,
        "appium:adbExecTimeout": 60000,
        "appium:newCommandTimeout": 120,
        "appium:uiautomator2ServerLaunchTimeout": 60000,
        "appium:uiautomator2ServerInstallTimeout": 60000
    })

    # Conecta ao servidor Appium
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    # Entrega o driver para o teste
    yield _driver

    # Encerra o driver ao final do teste
    print("\nEncerrando o driver...")
    _driver.quit()


@pytest.fixture(scope="session")
def appium_test_capabilities():
    """Lê o JSON de capabilities e retorna como dicionário"""
    json_path = Path(__file__).parent / "data" / "data_test.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
