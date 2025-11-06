from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from .base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver,20)
        self.product_quanty = 'new UiSelector().className("android.widget.EditText")'
        self.validate_name_cart = 'new UiSelector().resourceId("Card Produto")'
        self.subtotal_price = 'new UiSelector().className("android.view.View").descriptionMatches("R\\$.*").instance(0)'
        self.total_price = 'new UiSelector().className("android.view.View").descriptionMatches("R\\$.*").instance(1)'
        self.total_price_checkout = 'new UiSelector().resourceId("Fechar pedido")'
        self.place_order = 'new UiSelector().resourceId("Fechar pedido")'
        self.validate_message_email = 'new UiSelector().description("Informe seu e-mail para continuar")'
       


    def validate_totals_and_finish(self, expected_price):
        
        expected_total = float(expected_price.replace('.', '').replace(',', '.')) * 2

        self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        logging.info("Scroll realizado")

        subtotal_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.subtotal_price).get_attribute("contentDescription")
        subtotal = float(subtotal_text.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').replace('- ', '-').strip())

        assert subtotal == expected_total, f"Subtotal errado: esperado={expected_total}, app={subtotal}"
        logging.info(f"Subtotal confirmado: {subtotal:.2f}")

        total_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price).get_attribute("contentDescription")
        total_app = float(total_text.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').replace('- ', '-').strip())

        assert total_app == expected_total, f"Total errado: esperado={expected_total}, app={total_app}"
        logging.info(f"Total correto: {total_app:.2f}")

        total_checkout_text = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, self.total_price_checkout).get_attribute("contentDescription")
        total_checkout = float(total_checkout_text.replace('R$', '').replace('fechar pedido', '').replace('\n', '').replace('.', '').replace(',', '.').replace('- ', '-').strip())
 
        assert total_checkout == expected_total, f"Total checkout divergente: esperado={expected_total}, app={total_checkout}"
        logging.info(f"Total checkout confirmado: {total_checkout:.2f}")

        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.place_order)
        logging.info("Botão 'Fechar pedido' clicado")

        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, self.validate_message_email)))
        assert element.is_displayed(), "Mensagem 'Informe seu e-mail para continuar' não exibida"
        logging.info("Mensagem de login exibida com sucesso")
