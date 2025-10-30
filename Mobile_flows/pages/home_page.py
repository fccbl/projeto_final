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
      self.apple_iphone = "Apple iPhone 17 Pro 256GB Laranja-cósmico"
      self.allow_americanas = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
      self.input_search = "//*[@hint='busque aqui seu produto']"
      self.click_text_box = "android.widget.EditText"
      self.product_title_on_details = "//android.widget.TextView[1]"
      self.dynamic_product_click_template = "//*[@text='{0}' or @content-desc='{0}']"


  

    def open_americanas(self):
       logging.info("O aplicativo das Americanas foi aberto")

    def search_products_1(self):
        product = get_wishlist_products()
        get_product = product[0]["Product"]
        logging.info(f"O primeiro produto da API é:{get_product}")
        
        # Clica no campo de busca (aguarda até estar presente)
        self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
        self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
        logging.info("Clicando no campo de busca")

        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))
        self.send_keys_to_element(AppiumBy.XPATH, self.input_search, get_product + Keys.ENTER)
        logging.info("Buscando o produto no campo de busca")
       
        try:
            # Tenta encontrar e clicar no primeiro resultado (o produto)
            self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.apple_iphone)))
            self.click_element(AppiumBy.ACCESSIBILITY_ID, self.apple_iphone)
            logging.info(f"Produto: {get_product} encontrado e clicado.")

        except TimeoutException:
            # Captura a exceção se o produto não for encontrado no tempo limite
            logging.error(f"O produto '{get_product}' NÃO FOI ENCONTRADO na tela de resultados.")

    def search_products_2(self):
          product = get_wishlist_products()
          get_product = product[1]["Product"]
          logging.info(f"O segundo do produto da API é:{get_product}")





    
    













      #  try:
      #   # Clica na barra de busca
      #      self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
      #      logging.info("Barra de busca clicada.")

      #   # Espera o campo de input aparecer
      #     self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))

      #   # Digita o nome do produto
      #     self.send_keys_to_element(AppiumBy.XPATH, self.input_search, product_name)
      #     logging.info(f"Nome do produto '{product_name}' digitado.")

      #   # Pressiona ENTER
      #      self.send_keys_to_element(AppiumBy.CLASS_NAME, self.click_text_box, Keys.ENTER)
      #      logging.info("Busca submetida (ENTER).")

      #   # Clica no produto encontrado
      #      exact_xpath = self.dynamic_product_click_template.format(product_name)
      #      self.click_element(AppiumBy.XPATH, exact_xpath)
      #      logging.info(f"✅ Produto '{product_name}' encontrado e clicado no app.")

      #      return product_name
      #     except Exception as e:
      #     blogging.error(f"❌ Erro ao buscar produto '{product_name}': {str(e)}")
      #       return None


  #  def validate_product_name(self, expected_name):
      #  element_name = self.get_element_text(AppiumBy.ANDROID_UIAUTOMATOR, self.expected_name_iphone)
      #  logging.info(f"📱 Nome no app: {element_name}")
      #  logging.info(f"🌐 Nome da API: {expected_name}")

      #  assert expected_name.lower() in element_name.lower(), \
      #    f"❌ O nome do produto no app ('{element_name}') não corresponde ao da API ('{expected_name}')"

      #  logging.info("✅ O produto exibido no app corresponde ao produto da API!")
       