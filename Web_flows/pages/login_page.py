from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import pyperclip
import time

class LoginPage():
     def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 54)
        self.email_login = (By.NAME, "email")
        self.send_button = (By.CSS_SELECTOR,"button.vtex-button[type='submit']") 
        self.codigo_email_message = (By.CSS_SELECTOR, "span[data-qa='message-subject']")
        self.code_message = (By.CSS_SELECTOR, "h1[data-qa='message-subject']")
        self.confirm_button = (By.CSS_SELECTOR, "button[type=submit]")
        self.codigo_input = (By.NAME, "token")
        self.button_copy = (By.CSS_SELECTOR, "button[data-qa='copy-button']")
        self.validade_email_header = (By.CSS_SELECTOR,".ButtonLogin_textContainer__7NZHr span:first-child")


     def open_temp_mail_tab(self, temp_mail_url):
        self.driver.switch_to.new_window('tab')
        self.driver.get(temp_mail_url)
        logging.info("Nova aba aberta: Temp-Mail")

     def get_temp_email(self):
      self.wait.until(EC.element_to_be_clickable(self.button_copy)).click()
      # Copia e-mail do clipboard
      email = pyperclip.paste()
      logging.info(f"E-mail temporário copiado: {email}")
      return email

     def return_to_login_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        logging.info("Voltando para a aba da Americanas")

     def email_input(self, email):
        campo_email_americanas = self.wait.until(EC.visibility_of_element_located(self.email_login))
        campo_email_americanas.send_keys(email)
        logging.info(f"E-mail {email} preenchido no campo de login")

     def button_send_email(self):
        button = self.wait.until(EC.element_to_be_clickable(self.send_button))
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
          # Espera um instante pra garantir que nada está sobreposto
        time.sleep(1)
        button.click()
        logging.info("Clique no botão Enviar realizado")
 
     def return_to_temp_mail_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        logging.info("Voltando para a aba do Temp-Mail")


     def get_access_code(self):
      self.wait.until(EC.visibility_of_element_located(self.codigo_email_message)).click()
      message_element = self.wait.until(EC.visibility_of_element_located(self.code_message))
      message_text = message_element.text
      code_str = message_text.split()[-1]
      code_int = int(code_str)
      logging.info(f"Código de acesso capturado: {code_int}")
      return code_int

     
     def return_to_login_tab_after_code(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        logging.info("Voltando para a aba da Americanas após pegar o código")

     def codigo_input_field(self, code):
        campo_codigo = self.wait.until(EC.visibility_of_element_located(self.codigo_input))
        campo_codigo.send_keys(code)
        logging.info(f"Código {code} preenchido no campo de verificação")

     def button_confirm_code(self):
          self.wait.until(EC.element_to_be_clickable(self.confirm_button)).click()
          logging.info("Clique no botão Confirmar realizado")
     
     def validate_homepage(self, url):
      time.sleep(40)
      try:
        current = self.driver.current_url
        assert url in current
        logging.info(f"HomePage validada com sucesso: {current}")
        return True
      except AssertionError:
        logging.error(f"URL inesperada: {current}, esperado conter: {url}")
        return False
      except Exception as e:
        logging.error(f"Erro ao validar homepage: {e}")
        return False


     def validate_login(self, email):
      try:
        element = self.wait.until(EC.visibility_of_element_located(self.validade_email_header))
        header_text = element.text
        logging.info(f"Email do usuário validado no cabeçalho: '{header_text}'")
        return email.split("@")[0] in header_text
      except Exception as e:
        logging.error(f"Erro ao validar login: {e}")
        return False

      





        