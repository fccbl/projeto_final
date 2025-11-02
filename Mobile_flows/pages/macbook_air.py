from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support.ui import WebDriverWait
from api_utils import get_wishlist_products
from selenium.common.exceptions import TimeoutException


class Third_Product(BasePage):
    def __init__(self, driver):
      super().__init__(driver)
      self.wait = WebDriverWait(driver,10)
      self.input_search = "//*[@hint='busque aqui seu produto']"
      self.search_box = "busque aqui seu produto"
      self.macbook = 'new UiSelector().descriptionContains("MacBook Air 13, M3")'
      self.macbook_validate = 'new UiSelector().description("Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite")'
      self.macbook_price = 'new UiSelector().description("R$ 18.589,00")'
      self.input_zip_code = 'new UiSelector().resourceId("Digite o CEP")'
      self.calculator_zip_code = "Calcular"
      self.alert_zip_code= "Snackbar alerta"
      self.by_button = 'new UiSelector().resourceId("Comprar agora")'
      self.validate_poupup = "Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite\nDe R$ 21.055,35\nPor R$ 18.589,00"
      self.increase_quantify = '//android.widget.ImageView[@resource-id="Aumentar quantidade em 1"]'
      self.two_quantify = 'new UiSelector().className("android.widget.EditText")'






    def search_products_3(self):
        product = get_wishlist_products()
        get_product = product[2]["Product"]
        logging.info(f"O terceiro produto da API é:{get_product}")


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

        return get_product
    
    def validade_name_price(self):
        product = get_wishlist_products()
        get_product = product[2]["Product"]
        price_product = product[2]["Price"]

        mac_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_validate).get_attribute("contentDescription")
        assert get_product == mac_text
        logging.info("Nome de produto validado")

        price_app =self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_price).get_attribute("contentDescription")
        price_americanas = price_app.replace("R$", "").strip()
        assert price_americanas == price_product
        logging.info("Preço validado")

    def validade_zip_code(self):
        zip_code_api= get_wishlist_products()
        input_zip_code_api = zip_code_api[2]["Zipcode"]

        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        logging.info("Scroll")
        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        logging.info("ZipCode clicado")
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR,self.input_zip_code, "00000000")
        logging.info("Introduzi um cep invalido")


        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
        logging.info("Mensagem de frete indisponivel na tela")
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, self.input_zip_code)
        logging.info("Cep valido digitado")

    def buy_product(self):
       self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.by_button)
       logging.info("Botao comprar clicado")

    def cart_poup_up(self):
        product = get_wishlist_products()
        name_product = product[2]["Product"]
        price_product = product[2]["Price"]

        element_poup_up = self.find_element(AppiumBy.ACCESSIBILITY_ID, self.validate_poupup)
        validate_poup_up= element_poup_up.get_attribute("contentDescription")

        assert name_product in validate_poup_up, f" Nome divergente: API={name_product}, App={validate_poup_up}"
        logging.info("Confirmando o nome do produto no cart poup-up")
        assert price_product in validate_poup_up, f" Preço divergente: API={price_product}, App={validate_poup_up}"
        logging.info("Confirmando o preço do produto no cart poup-up")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.increase_quantify))).click()
        logging.info("Clique no +")

        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.two_quantify)))
        quantify_text = element.get_attribute("text")
        content_desc = element.get_attribute("contentDescription")
        logging.info(f"🧩 Texto da quantidade: '{quantify_text}', contentDescription: '{content_desc}'")