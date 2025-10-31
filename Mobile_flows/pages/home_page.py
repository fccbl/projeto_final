from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support.ui import WebDriverWait
from api_utils import get_wishlist_products
from selenium.common.exceptions import TimeoutException




class HomePage(BasePage):
    def __init__(self, driver):
      super().__init__(driver)
      self.wait = WebDriverWait(driver,10)
      self.search_box = "busque aqui seu produto"
      self.apple_iphone = 'new UiSelector().descriptionContains("iPhone 17 Pro 256GB Laranja-cósmico")'
      self.allow_americanas = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
      self.input_search = "//*[@hint='busque aqui seu produto']"
      self.click_text_box = "android.widget.EditText"
      self.product_title_on_details = "//android.widget.TextView[1]"
      self.apple_watch = 'new UiSelector().descriptionContains("Apple Watch se gps Caixa prateada de alumínio")'
      self.macbook = 'new UiSelector().descriptionContains("MacBook Air 13")'



    #def open_americanas(self):
     #  logging.info("O aplicativo das Americanas foi aberto")

    def search_products_1(self):
        product_name = get_wishlist_products()[0]["Product"]
        logging.info(f"O primeiro produto da API é: {product_name}")

      
        self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
        self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))
        self.send_keys_to_element(AppiumBy.XPATH, self.input_search, product_name)
        logging.info("Buscando o produto no campo de busca")
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.apple_iphone))).click()
            logging.info(f"✅ Produto '{product_name}' encontrado e clicado.")
        except TimeoutException:
            logging.error(f"❌ Produto '{product_name}' não encontrado.")
            self.driver.back()
            logging.info("Voltando à tela inicial para tentar próxima busca.")
            return product_name

    def search_products_2(self):
          product = get_wishlist_products()
          get_product = product[1]["Product"]
          logging.info(f"O segundo do produto da API é:{get_product}")

          self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
          self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
          self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))
          self.send_keys_to_element(AppiumBy.XPATH, self.input_search, get_product + Keys.ENTER)
          logging.info("Buscando o produto no campo de busca")

          try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.apple_watch))).click()
            logging.info(f"✅ Produto '{get_product}' encontrado e clicado.")
          except TimeoutException:
            logging.error(f"❌ Produto '{get_product}' não encontrado.")
            self.driver.back()
          return get_product
    
    def search_products_3(self):
          product = get_wishlist_products()
          get_product = product[2]["Product"]
          logging.info(f"O terceiro do produto da API é:{get_product}")

          self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
          self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
          self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))

          self.send_keys_to_element(AppiumBy.XPATH, self.input_search, get_product + Keys.ENTER)
          logging.info("Buscando o produto no campo de busca")

          try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.macbook))).click()
            logging.info(f"✅ Produto '{get_product}' encontrado e clicado.")
          except TimeoutException:
            logging.error(f"❌ Produto '{get_product}' não encontrado.")
            self.driver.back()
          return get_product











