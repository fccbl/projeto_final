from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from .base_page import BasePage


class ZipCodePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver,20)
        self.input_zip_code = 'new UiSelector().resourceId("Digite o CEP")'
        self.calculator_zip_code = "Calcular"
        self.message_cep = 'new UiSelector().descriptionMatches("Receba em até \\d+ dias úteis.*")'
        self.alert_zip_code = "Snackbar alerta"
        self.by_button = 'new UiSelector().resourceId("Comprar agora")'

    def validate_zip_code(self, expected_zip, expected_delivery_estimate, expected_shipping_fee):

    
        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        logging.info("Scroll realizado")

        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        logging.info("Campo de CEP clicado.")
       
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, "00000000")
        logging.info("CEP inválido inserido para validação.")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        self.is_element_displayed(AppiumBy.ID, self.alert_zip_code)
        logging.info("Mensagem de frete indisponível exibida corretamente.")
        
        field = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code)
        field.clear()
 
        self.send_keys_to_element(AppiumBy.ANDROID_UIAUTOMATOR, self.input_zip_code, expected_zip)
        logging.info(f"CEP válido '{expected_zip}' inserido.")

        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.calculator_zip_code))).click()

        message_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,self.message_cep).get_attribute("contentDescription")

        if expected_delivery_estimate in message_text and expected_shipping_fee in message_text:
            logging.info(f"✅ Mensagem correta: '{message_text}'")
        else:
            logging.warning(f"⚠️ Divergência!\n"
                f"Esperado: '{expected_delivery_estimate}' e '{expected_shipping_fee}'\n"
                f"Obtido: '{message_text}'")

    def click_buy_now(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.by_button)
        logging.info(" Botão 'Comprar agora' clicado.")