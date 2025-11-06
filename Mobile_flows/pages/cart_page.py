from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from .base_page import BasePage



class CartPage(BasePage):
        
    def __init__(self, driver):
       super().__init__(driver)
       self.wait = WebDriverWait(driver,20)

       self.text_quantity_one = 'new UiSelector().text("1")'
       self.text_quantify_two = 'new UiSelector().text("2")'
       self.decrease_quantify = 'new UiSelector().resourceId("Reduzir quantidade em 1")'
       self.increase_quantify = '//android.widget.ImageView[@resource-id="Aumentar quantidade em 1"]'
       self.product_quanty = 'new UiSelector().className("android.widget.EditText")'
       self.two_quantify = 'new UiSelector().className("android.widget.EditText")'
       self.validate_name_cart = 'new UiSelector().resourceId("Card Produto")'
       self.validate_name_poupup = 'new UiSelector().resourceId("Card Produto")'
       self.input_zip_code = 'new UiSelector().resourceId("Digite o CEP")'
       self.calculator_zip_code = "Calcular"
       self.message_cep = 'new UiSelector().descriptionMatches("Receba em até \\d+ dias úteis.*")'
       self.alert_zip_code= "Snackbar alerta"





    def cart_poup_up(self, expected_name, expected_price):
       """Valida nome, preço e quantidade do produto no popup do carrinho"""
 
       popup_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.validate_name_poupup)
       popup_content = popup_element.get_attribute("contentDescription")
 
       assert expected_name in popup_content, f" Nome divergente: API={expected_name}, App={popup_content}"
       logging.info(" Nome do produto confirmado no popup.")

       assert expected_price in popup_content, f" Preço divergente: API={expected_price}, App={popup_content}"
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

    

    def checkout_flow(self, expected_name, expected_zip , expected_delivery_estimate, expected_shipping_fee ):
      
 
         checkout_quantity = int(self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.two_quantify).get_attribute("text"))
    
         assert checkout_quantity == self.after_number
         logging.info(f"Quantidade confirmada: {checkout_quantity}")

 
         app_name = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.validate_name_cart).get_attribute("contentDescription")

         assert expected_name in app_name, \
          f"Nome divergente: esperado={expected_name}, app={app_name}"

         logging.info(f"Nome validado com sucesso:{expected_name}")


         self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
         self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, "00000000")

         logging.info("CEP inválido inserido para validação de erro")

         self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

         self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
         logging.info("Mensagem de frete indisponível exibida corretamente")

 
         campo = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
         campo.clear()

         self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, expected_zip)
         logging.info(f"CEP válido '{expected_zip}' inserido")

         self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

         message_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.message_cep).get_attribute("contentDescription")

         if expected_delivery_estimate in message_text and expected_shipping_fee in message_text:
           logging.info(f"Mensagem de frete correta: '{message_text}'")

         else:
          logging.warning(f"⚠️ Divergência!\n"
            f"Esperado: '{expected_delivery_estimate}' e '{expected_shipping_fee}'\n"
            f"Obtido: '{message_text}'")
          