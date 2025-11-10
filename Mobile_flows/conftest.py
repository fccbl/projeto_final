import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions
import os
import time
from pathlib import Path
import allure



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
        "appium:uiautomator2ServerInstallTimeout": 60000,
        "appium:autoGrantPermissions": True,
        "appium:connectHardwareKeyboard": True,  # Allows physical keyboard
        "appium:unicodeKeyboard": True,
        "appium:resetKeyboard": True              
    })

    # Conecta ao servidor Appium
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    # Entrega o driver para o teste
    yield _driver

    # Encerra o driver ao final do teste
    print("\nEncerrando o driver...")
    _driver.quit()




LOG_FILE = Path("test_durations.log")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Marca o início do teste e registra no log."""
    item.start_time = time.time()
    item.start_str = time.strftime("%H:%M:%S", time.localtime())
    msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    """Marca o fim do teste e registra a duração."""
    duration = time.time() - item.start_time
    msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tira screenshot automaticamente em caso de falha."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" and report.failed:
        os.makedirs("screenshots", exist_ok=True)
        driver = item.funcargs['driver']
        screenshot_file = os.path.join("screenshots", f"{item.name}_error.png")
        driver.save_screenshot(screenshot_file)

        # 📸 Adiciona screenshot no Allure
        if os.path.exists(screenshot_file):
            with open(screenshot_file, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"{item.name}_error",
                    attachment_type=allure.attachment_type.PNG
                )
  