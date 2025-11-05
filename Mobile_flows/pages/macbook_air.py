from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support.ui import WebDriverWait
from api_utils import get_wishlist_products
from selenium.common.exceptions import TimeoutException
import time


class Third_Product(BasePage):
    def __init__(self, driver):
      super().__init__(driver)
      self.wait = WebDriverWait(driver,20)
      self.input_search = "//*[@hint='busque aqui seu produto']"
      self.search_box = "busque aqui seu produto"
      self.macbook = 'new UiSelector().descriptionContains("MacBook Air 13, M3")'
      self.macbook_validate = 'new UiSelector().descriptionContains("Apple MacBook Air 13")'
      self.macbook_price = 'new UiSelector().descriptionContains("R$").instance(1)'
      self.input_zip_code = 'new UiSelector().resourceId("Digite o CEP")'
      self.calculator_zip_code = "Calcular"
      self.alert_zip_code= "Snackbar alerta"
      self.by_button = 'new UiSelector().resourceId("Comprar agora")'
      self.macbook_name_validate = 'new UiSelector().descriptionContains("Apple MacBook Air 13")'
      self.increase_quantify = '//android.widget.ImageView[@resource-id="Aumentar quantidade em 1"]'
      self.two_quantify = 'new UiSelector().text("2")'
      self.message_cep = 'new UiSelector().descriptionMatches("Receba em até \\d+ dias úteis.*")'
      self.one_quantify = 'new UiSelector().text("1")'
      self.decrease_quantify = 'new UiSelector().resourceId("Reduzir quantidade em 1")'
      self.subtotal = 'new UiSelector().descriptionStartsWith("R$")'
      self.total = 'new UiSelector().descriptionStartsWith("R$").instance(1)'
      self.place_order = 'new UiSelector().resourceId("Fechar pedido")'
      self.total_price_checkout = 'new UiSelector().resourceId("Fechar pedido")'
      self.validate_message_email = 'new UiSelector().description("Informe seu e-mail para continuar")'
      self.text_quantity_one = 'new UiSelector().text("1")'
      self.text_quantify_two = 'new UiSelector().text("2")'
      self.product_quanty = 'new UiSelector().className("android.widget.EditText")'
      self.subtotal_price = 'new UiSelector().className("android.view.View").descriptionMatches("R\\$.*").instance(0)'
      self.total_price = 'new UiSelector().className("android.view.View").descriptionMatches("R\\$.*").instance(1)'



    def search_products_3(self):
        """Busca o primeiro produto retornado pela API e o seleciona no app."""

        product = get_wishlist_products()
        get_product = product[2]["Product"]
        logging.info(f"O terceiro produto da API é:{get_product}")


        self.wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.search_box)))
        self.click_element(AppiumBy.ACCESSIBILITY_ID, self.search_box)
        self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.input_search)))
        self.send_keys_to_element(AppiumBy.XPATH, self.input_search, get_product)
        logging.info("Buscando o produto no campo de busca")


        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.macbook))).click()
            logging.info(f"✅ Produto '{get_product}' encontrado e clicado.")
        except TimeoutException:
            logging.error(f"❌ Produto '{get_product}' não encontrado.")

        
    
    def validate_name_price(self):
        """Valida se o nome e o preço do produto exibidos no app correspondem aos valores retornados pela API.""" 

        products_from_api = get_wishlist_products()
        expected_product_name  = products_from_api[2]["Product"]
        expected_product_price = products_from_api[2]["Price"]

        app_product_name= self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_validate).get_attribute("contentDescription")
        assert expected_product_name == app_product_name, f"Nome divergente. Esperado: '{expected_product_name}', Obtido: '{app_product_name}'"
        logging.info(f"Nome do produto validado com sucesso: '{app_product_name}'.")

        app_price_text =self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_price).get_attribute("contentDescription")
        app_price_clean = app_price_text.replace("R$", "").strip()
        assert app_price_clean == expected_product_price, f"Preço divergente. Esperado: '{expected_product_price}', Obtido: '{app_price_clean}'"
        logging.info(f"Preço do produto validado com sucesso: '{app_price_clean}'.")

    def validate_zip_code(self):
         """Valida o comportamento do campo de CEP, testando um CEP inválido e um válido da API."""

         products_from_api = get_wishlist_products()[2]
         expected_zip_code  = products_from_api["Zipcode"]
         api_delivery_estimate = products_from_api["delivery_estimate"]
         delivery_days = products_from_api["shipping_fee"]

         self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
         logging.info("Scroll realizado") 

         self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
         self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
         logging.info(" Campo de CEP clicado.")

         self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR,self.input_zip_code, "00000000")
         logging.info("CEP inválido inserido para validação de erro.")

         self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()
         self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
         logging.info("Mensagem de frete indisponível exibida corretamente.")

         campo = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        
         campo.clear()

         self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, expected_zip_code)
         logging.info(f" CEP válido '{expected_zip_code}' inserido no campo.")

         self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

         message_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.message_cep)
         message_text = message_element.get_attribute("contentDescription")

         if api_delivery_estimate in message_text and delivery_days in message_text:
          logging.info(f"✅ Mensagem exibida corretamente: '{message_text}'")
         else:
          logging.warning(f"⚠️ Divergência na mensagem.\n"
          f"Esperado: '{api_delivery_estimate}' e '{delivery_days}'\n"
           f"Obtido: '{message_text}'")
      

    def buy_product(self):
       """Clica no botão 'Comprar agora' para iniciar o processo de compra do produto."""

       self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.by_button)
       logging.info(" Botão 'Comprar agora' clicado com sucesso.")

    def cart_poup_up(self):
        """Valida nome do produto no popup do carrinho ."""
     

        product_api  = get_wishlist_products()[2]
        api_name, api_price = product_api["Product"], product_api["Price"]

        popup_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_name_validate)
        popup_content = popup_element.get_attribute("contentDescription")
 
        assert api_name in popup_content, f" Nome divergente: API={api_name}, App={popup_content}"
        logging.info(" Nome do produto confirmado no popup.")

        assert api_price in popup_content, f" Preço divergente: API={api_price}, App={popup_content}"
        logging.info("Preço do produto confirmado no popup.")

        
    def validate_quantity_change(self):
        """Valida se a quantidade do produto no carrinho é atualizada após clicar no botão '+'."""

        before_number = int(self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.text_quantity_one).text)
        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.increase_quantify))).click()
        logging.info("Clique no botão '+'.")

        self.after_number = int(self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.text_quantify_two).text)
        assert self.after_number == before_number + 1
        logging.info(f"Quantidade atualizada para {self.after_number} no carrinho.")
        

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, self.decrease_quantify))).click()
        logging.info("Quantidade atualizada para 1.")


        # Captura o valor antes e depois do clique
        initial_quantity = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.product_quanty).get_attribute("text")
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.decrease_quantify)
        final_quantity = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.product_quanty).get_attribute("text")

        assert initial_quantity == final_quantity, f"O botão '-' parece estar ativo — quantidade mudou de {initial_quantity} para {final_quantity}"
        logging.info(f" Botão '-' está inativo — quantidade permaneceu em {initial_quantity}")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.increase_quantify))).click()
        logging.info("Clique no botão '+'.")
     
        

    def click_checkout(self):
       """Realiza o clique no botão 'Finalizar compra' usando coordenadas fixas."""

       x, y = 500, 2050
       self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
       logging.info(f"Clique no botão 'Finalizar compra'.")

    def page_car(self):
        """Valida o carrinho confirmando nome, preços, quantidade, CEPs e a exibição da tela de login/check-out."""
        
        product = get_wishlist_products()[2]
        api_delivery_estimate = product["delivery_estimate"]
        delivery_days = product["shipping_fee"]
        api_name = product["Product"]
        api_price = float(product["Price"].replace('.', '').replace(',', '.'))
        api_zip = product["Zipcode"]
        expected_total = api_price * 2
     
        checkout_quantity = int(self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.two_quantify).get_attribute("text"))
        assert checkout_quantity == self.after_number
        logging.info(f"Quantidade confirmada no checkout: {checkout_quantity}.")
    

        app_name = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.macbook_name_validate).get_attribute("contentDescription")
        assert api_name in app_name, f"❌ Nome divergente: API={api_name}, App={app_name}"
        logging.info("Nome do produto validado no carrinho")

        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR,self.input_zip_code, "00000000")
        logging.info("CEP inválido inserido para validação de erro.")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
        logging.info("Mensagem de frete indisponível exibida corretamente.")

        campo = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        
        campo.clear()   

        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, api_zip)
        logging.info(f" CEP válido '{api_zip}' inserido no campo.")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        message_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.message_cep)
        message_text = message_element.get_attribute("contentDescription")

        if api_delivery_estimate in message_text and delivery_days in message_text:
          logging.info(f"✅ Mensagem exibida corretamente: '{message_text}'")
        else:
          logging.warning(f"⚠️ Divergência na mensagem.\n"
          f"Esperado: '{api_delivery_estimate}' e '{delivery_days}'\n"
           f"Obtido: '{message_text}'")

        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        logging.info("Scroll realizado")

        
        subtotal_price_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.subtotal_price).get_attribute("contentDescription")
        subtotal_price = float(subtotal_price_text.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').replace('- ', '-').strip())
        
        assert subtotal_price == expected_total, f"Valor esperado era {expected_total}, mas foi {subtotal_price}"
        logging.info(f" Subtotal confirmado: {subtotal_price:.2f} (dobro do unitário {expected_total / 2:.2f})")

        total_price_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price).get_attribute("contentDescription")
        total_price_app = float(total_price_text.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').replace('- ', '-').strip())

        assert total_price_app == expected_total, f"Valor esperado era {expected_total}, mas foi {total_price_app}"
        logging.info(f" Total confirmado: {total_price_app:.2f} (dobro do unitário {expected_total / 2:.2f})")

        total_checkout_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price_checkout).get_attribute("contentDescription")
        total_app = total_checkout_text.replace('R$', '').replace('fechar pedido', '').replace('\n', '').replace('.', '').replace(',', '.').replace('- ', '-').strip()
        total_checkout = float(total_app)

        assert total_checkout == expected_total, f"Valor total divergente! Esperado: {expected_total}, App: {total_app}"
        logging.info(f"✅ Total do checkout confirmado: {total_checkout:.2f} (dobro do unitário {expected_total / 2:.2f})")

        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.place_order)
        logging.info("Clique check-out")

        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.validate_message_email)))


        assert element.is_displayed(), " Mensagem 'Informe seu e-mail para continuar' não foi exibida!"
        logging.info(" Mensagem 'Informe seu e-mail para continuar' exibida na tela.")
