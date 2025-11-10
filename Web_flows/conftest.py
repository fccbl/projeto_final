import pytest
import csv
from selenium import webdriver
import os
import time
from pathlib import Path
import allure

@pytest.fixture
def driver():
    """
   Create a Chrome instance"
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
  