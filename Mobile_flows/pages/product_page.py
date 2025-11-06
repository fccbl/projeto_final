from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging
from .base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver,20)
        self.search_box = "busque aqui seu produto"
        self.input_search = "//*[@hint='busque aqui seu produto']"
        self.price_locator = 'new UiSelector().descriptionMatches("R\\$.*\\d{1,3}\\.\\d{3},\\d{2}")'
        self.validate_name_poupup = 'new UiSelector().resourceId("Card Produto")'

    def search_product(self, product_name):
        logging.info(f"🔎 Buscando produto: {product_name}")

        self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
        self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)

        self.send_keys_to_element(AppiumBy.XPATH, self.input_search, product_name)
        logging.info(f"✅ '{product_name}' inserido no campo de busca.")

        product_locator = f'new UiSelector().descriptionContains("{product_name}")'

        try:
            product_el = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, product_locator)))
            product_el.click()
            logging.info(f"✅ Produto '{product_name}' encontrado e clicado.")
        except TimeoutException:
            logging.error(f"❌ Produto '{product_name}' não encontrado.")
            raise

    def validate_name_price(self, expected_name, expected_price):
        name_locator = f'new UiSelector().descriptionContains("{expected_name}")'

        app_product_name = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, name_locator).get_attribute("contentDescription")
        assert expected_name in app_product_name, f"Nome divergente. Esperado='{expected_name}'. App='{app_product_name}'"
        logging.info(f"✅ Nome validado: '{app_product_name}'")

        price_elements = self.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, self.price_locator)
        if not price_elements:
            raise AssertionError("❌ Nenhum preço encontrado na tela!")

        price_app = price_elements[-1].get_attribute("contentDescription")
        clean_app = price_app.replace("R$", "").replace(".", "").replace(",", ".").strip()
        clean_expected = expected_price.replace("R$", "").replace(".", "").replace(",", ".").strip()

        assert clean_app == clean_expected, f"Preço divergente. Esperado='{expected_price}', App='{clean_app}'"
        logging.info(f"✅ Preço validado: '{clean_app}'")


