from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support.ui import WebDriverWait
from api_utils import get_wishlist_products
from selenium.common.exceptions import TimeoutException




class First_Product(BasePage):
    def __init__(self, driver):
      super().__init__(driver)
      self.wait = WebDriverWait(driver,10)
      self.search_box = "busque aqui seu produto"
      self.apple_iphone = 'new UiSelector().descriptionContains("iPhone 17 Pro 256GB Laranja-cósmico")'
      self.input_search = "//*[@hint='busque aqui seu produto']"
      self.click_text_box = "android.widget.EditText"
      self.iphone_validate = 'new UiSelector().description("Apple iPhone 17 Pro 256GB Laranja-cósmico")'
      self.iphone_cart_poup_up= "Apple iPhone 17 Pro Max 256GB Laranja-cósmico\nR$ 13.498,80"
      self.iphone_price = 'new UiSelector().description("R$ 12.418,80")'
      self.input_zip_code = 'new UiSelector().resourceId("Digite o CEP")'
      self.alert_zip_code= "Snackbar alerta"
      self.by_button = 'new UiSelector().resourceId("Comprar agora")'
      self.increase_quantify = '//android.widget.ImageView[@resource-id="Aumentar quantidade em 1"]'
      self.decrease_quantify = 'new UiSelector().resourceId("Reduzir quantidade em 1")'
      self.two_quantify = 'new UiSelector().className("android.widget.EditText")'
      self.iphone_name_validate = 'new UiSelector().resourceId("Card Produto")'
      self.calculator_zip_code = "Calcular"
      self.access_cart = self.access_cart = 'new UiSelector().resourceId("adicionar e ir para a cesta")'
      self.validate_name_cart = 'new UiSelector().resourceId("Card Produto")'
      self.validate_quantify_cart = 'new UiSelector().text("2")'
      self.add_cart = 'new UiSelector().resourceId("adicionar e continuar comprando")'
      self.car = 'new UiSelector().resourceId("Carrinho")'
      self.subtotal_price = 'new UiSelector().className("android.view.View").index(4)'
      self.total_price = 'new UiSelector().resourceId("Fechar pedido")'
      self.validate_message_email = 'new UiSelector().description("Informe seu e-mail para continuar")'

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

    
    def validade_name_price(self):
        product = get_wishlist_products()
        get_product = product[0]["Product"]
        price_product = product[0]["Price"]

        app_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.iphone_validate).get_attribute("contentDescription")
        assert get_product == app_text
        logging.info("Nome de produto validado")

        price_app =self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.iphone_price).get_attribute("contentDescription")
        price_americanas = price_app.replace("R$", "").strip()
        assert price_americanas == price_product
        logging.info("Preço validado")

    def validade_zip_code(self):
        zip_code_api= get_wishlist_products()
        code_api = zip_code_api[0]["Zipcode"]

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
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, code_api)
        logging.info("Cep valido digitado")
      

    def buy_product(self):
       self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.by_button)
       logging.info("Botao comprar clicado")


    def cart_poup_up(self):
        product = get_wishlist_products()
        name_product = product[0]["Product"]
        price_product = product[0]["Price"]

        element_poup_up = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.iphone_name_validate)
        validate_poup_up= element_poup_up.get_attribute("contentDescription")

        assert name_product in validate_poup_up, f" Nome divergente: API={name_product}, App={validate_poup_up}"
        logging.info("Confirmando o nome do produto no cart poup-up")
        assert price_product in validate_poup_up, f" Preço divergente: API={price_product}, App={validate_poup_up}"
        logging.info("Confirmando o preço do produto no cart poup-up")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.increase_quantify))).click()
        logging.info("Clique no +")

        self.wait.until(EC.text_to_be_present_in_element((AppiumBy.ANDROID_UIAUTOMATOR, self.two_quantify), "2"))
        logging.info("Quantidade atualizada para 2")
    
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, self.decrease_quantify))).click()
        logging.info("Diminuindo 1 quantifade")

        # cart_button= self.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, self.decrease_quantify)))
        # assert not cart_button.is_enabled()
        # logging.info(f"Estado do botão: {cart_button.is_enabled()}")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.increase_quantify))).click()
        logging.info("Clique no +")

        self.wait.until(EC.text_to_be_present_in_element((AppiumBy.ANDROID_UIAUTOMATOR, self.two_quantify), "2"))
        logging.info("Quantidade atualizada para 2")

    def go_to_cart(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.add_cart)
        logging.info("adicionando o produto para a tela de carrinho")

        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.car)


 
    def page_car(self):
        product = get_wishlist_products()
        name_product_expected = product[0]["Product"]
        price_product_expect = product[0]["Price"]
        code_api = product[0]["Zipcode"]
       
        #Converte a string "12.418,80" em número 12418.80
        price_product_expect = float(price_product_expect.replace('.', '').replace(',', '.'))
        total_price = price_product_expect * 2

        element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.validate_name_cart)
        name_product_app= element.get_attribute("contentDescription")

        assert name_product_expected in name_product_app, f" Nome divergente: API={name_product_expected}, App={name_product_app}"
        logging.info("Confirmando o nome do produto no carrinho")

        self.wait.until(EC.text_to_be_present_in_element((AppiumBy.ANDROID_UIAUTOMATOR, self.validate_quantify_cart), "2"))
        logging.info("Quantidade igual a 2")

        price = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.subtotal_price).get_attribute("contentDescription")
        price = float(price.replace('R$', '').replace('Por', '').replace('\xa0', '').replace('.', '').replace(',', '.').strip())


        assert price == total_price, f"Valor esperado era {total_price}, mas foi {price}"
        logging.info("Confirmando o valor subtotal o dobro do valor unitario")

        total_price_app = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price).get_attribute("contentDescription")
        total_price_app = total_price_app.replace('R$', '').replace('fechar pedido', '').replace('\n', '').replace('.', '').replace(',', '.').strip()
        total_price_app = float(total_price_app)

        assert total_price_app == total_price, f"Valor total divergente! Esperado: {total_price}, App: {total_price_app}"
        logging.info("Confirmando que o valor total é o dobro do unitário")

        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR,self.input_zip_code, "00000000")
        logging.info("Introduzi um cep invalido")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
        logging.info("Mensagem de frete indisponivel na tela")
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, code_api)
        logging.info("Cep valido digitado")
      
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price)
        logging.info("Clique check-out")

      
        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.validate_message_email)))


        assert element.is_displayed(), "❌ Mensagem 'Informe seu e-mail para continuar' não foi exibida!"
        logging.info("✅ Mensagem 'Informe seu e-mail para continuar' exibida na tela.")

       




