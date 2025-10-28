from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import pyperclip
import time

class LoginPage():
     def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.email_login = (By.NAME, "email")
        self.send_button = (By.CSS_SELECTOR,"button.vtex-button[type='submit']") 
        self.codigo_email_message = (By.CSS_SELECTOR, "span[data-qa='message-subject']")
        self.code_message = (By.CSS_SELECTOR, "h1[data-qa='message-subject']")
        self.confirm_button = (By.CSS_SELECTOR, "button[type=submit]")
        self.codigo_input = (By.NAME, "token")
        self.button_copy = (By.CSS_SELECTOR, "button[data-qa='copy-button']")
        self.validade_email_header = (By.CSS_SELECTOR,".ButtonLogin_textContainer__7NZHr span:first-child")


     def open_temp_mail_tab(self, temp_mail_url):
      """Abre uma nova aba e navega para o Temp-Mail."""
      self.driver.switch_to.new_window('tab')
      self.driver.get(temp_mail_url)
      logging.info("Nova aba aberta: Temp-Mail")

     def get_temp_email(self):
      """Clica no botão de copiar e pega o e-mail temporário do clipboard."""
      self.wait.until(EC.element_to_be_clickable(self.button_copy)).click()
      email = pyperclip.paste()
      logging.info(f"E-mail temporário copiado: {email}")
      return email

     def return_to_login_tab(self):
        """Volta para a aba principal da Americanas."""
        self.driver.switch_to.window(self.driver.window_handles[0])
        logging.info("Voltando para a aba da Americanas")

     def email_input(self, email):
        """Preenche o campo de e-mail com o endereço fornecido."""
        campo_email_americanas = self.wait.until(EC.visibility_of_element_located(self.email_login))
        campo_email_americanas.send_keys(email)
        logging.info(f"E-mail {email} preenchido no campo de login")

     def button_send_email(self):
        """Clica no botão 'Enviar' para solicitar código de acesso."""
        button = self.wait.until(EC.element_to_be_clickable(self.send_button))
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
          # Espera um instante pra garantir que nada está sobreposto
        time.sleep(1)
        button.click()
        logging.info("Clique no botão Enviar realizado")
 
     def return_to_temp_mail_tab(self):
        """Volta para a aba do Temp-Mail para capturar o código."""
        self.driver.switch_to.window(self.driver.window_handles[1])
        logging.info("Voltando para a aba do Temp-Mail")


     def get_access_code(self):
       """
        Captura o código de acesso enviado por e-mail no Temp-Mail.
       1. Abre a mensagem de e-mail que contém o código.
       2. Lê o conteúdo da mensagem.
       3. Extrai o código (última palavra da mensagem).
       4. Converte para inteiro e retorna.
      """
       try: 
           self.wait.until(EC.element_to_be_clickable(self.codigo_email_message)).click()
           message_element = self.wait.until(EC.visibility_of_element_located(self.code_message))
           message_text = message_element.text
       #converter string para inteiro
           code_str = message_text.split()[-1]
           code_int = int(code_str)
           logging.info(f"Código de acesso capturado: {code_int}")
           return code_int
       except TimeoutException:
         error_message = f"❌ Erro de Timeout: O elemento da mensagem do código ({self.code_message}) não carregou a tempo."
         logging.error(error_message)
         return None
           
     def return_to_login_tab_after_code(self):
        """Volta para a aba principal da Americanas após capturar o código."""
        self.driver.switch_to.window(self.driver.window_handles[0])
        logging.info("Voltando para a aba da Americanas após pegar o código")

     def codigo_input_field(self, code):
      """Preenche o campo de código de verificação com o código fornecido."""
      try:
        campo_codigo = self.wait.until(EC.presence_of_element_located(self.codigo_input))
        self.wait.until(EC.visibility_of(campo_codigo))
        campo_codigo.send_keys(code)
        logging.info(f"Código {code} preenchido no campo de verificação")
      except Exception as e:
        logging.error(f"Falha ao preencher o código de verificação: {e}")
        raise

     def button_confirm_code(self):
          """Clica no botão 'Confirmar' para validar o código."""
          self.wait.until(EC.element_to_be_clickable(self.confirm_button)).click()
          logging.info("Clique no botão Confirmar realizado")
     
     def validate_homepage(self, expect_url):
      """Valida se a página atual é a homepage esperada."""
      time.sleep(7)
      try:
        # Espera até que a URL mude em relação à anterior
        self.wait.until(EC.url_changes(expect_url))
        current = self.driver.current_url
        logging.info(f"URL alterada com sucesso: {current}")
        return True
      except Exception as e:
        current = self.driver.current_url
        logging.error(f"A URL não mudou como esperado. Atual: {current}, anterior: {expect_url}. Erro: {e}")
        return False

     def validate_login(self, email):
      """Valida se o login foi realizado, verificando o cabeçalho."""
      expected_name = email.split("@")[0]
      try:
        # Espera até que o cabeçalho contenha o nome do usuário
        self.wait.until(EC.text_to_be_present_in_element(self.validade_email_header, expected_name))
        logging.info(f"Login validado: '{expected_name}' encontrado no cabeçalho")
        return True
      except Exception:
        logging.error(f"Login não validado: '{expected_name}' não encontrado")
        return False


      
      
      





        