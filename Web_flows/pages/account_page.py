from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging
import time

class MyAccountPage():
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.my_account_button = (By.CSS_SELECTOR, "span.ButtonLogin_myAccount__mte5i")
        self.email_validate = (By.CSS_SELECTOR, ".vtex-my-account-1-x-emailContainer > .vtex-my-account-1-x-dataEntryChildren")
        self.link_authentication = (By.CSS_SELECTOR, 'a.vtex-account_menu-link[href="#/authentication"]')
        self.set_password = (By.CSS_SELECTOR,"button.vtex-button[type='button'] > div.vtex-button__label")
        self.input_code = (By.CSS_SELECTOR, ".vtex-my-authentication-1-x-codeInput_container input")
        self.input_password = (By.CSS_SELECTOR, "input[type='password']")
        self.button = (By.XPATH, "//button[./div[text()='Salvar senha']]")
        self.success_field = (By.XPATH, "//div[text()='Senha']/following-sibling::div[contains(@class,'maskedPassword_content')]")
        self.password = "Abcdef12"
        self.container = (By.CSS_SELECTOR,".vtex-my-authentication-1-x-box_content")

    def account_button_click(self,email):
        """Clica no botão 'Minha Conta' e valida o e-mail exibido."""
        self.wait.until(EC.element_to_be_clickable(self.my_account_button)).click()
        logging.info("Clique no botão minha conta")
        account_email=self.wait.until(EC.visibility_of_element_located(self.email_validate)).text.strip()
        assert account_email == email
        logging.info("Email do usuário validado")

    def go_to_set_password(self):
     """
        Acessa a tela de 'Definir senha' clicando no link de autenticação.
        Inclui scroll para garantir que o elemento esteja visível.
        """
     try:
        link = self.wait.until(EC.element_to_be_clickable(self.link_authentication))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        link.click()
        logging.info("Link 'Autenticação' clicado.")

        self.wait.until(EC.element_to_be_clickable(self.set_password)).click()
        logging.info("Botão 'Definir senha' clicado com sucesso.")
     except Exception as e:
        logging.error(f"Erro ao acessar 'Definir senha': {e}")
        raise

        
    
    def enter_access_code(self,code):
        """Insere o código de acesso recebido por e-mail no campo apropriado."""
        try:
          input_field = self.wait.until(EC.presence_of_element_located(self.input_code))
          input_field.send_keys(code)
          logging.info(f"Código inserido:{code}")
        except Exception as e:
         logging.error(f"Falha ao inserir código de acesso: {e}")
         raise


    def test_password(self, password):
       """
        Testa a inserção de senha e verifica se o botão 'Salvar' está clicável.
        Limpa o campo antes e depois de cada teste.
        Retorna True se o botão puder ser clicado.
        """
       input = self.wait.until(EC.visibility_of_element_located(self.input_password))        
       input.send_keys(password)
       logging.info(f"Senha inserida: {password}")
       time.sleep(1.5)

       try:
        button_element =self.wait.until(EC.element_to_be_clickable(self.button))
        is_clickable = True
        button_element.click()
        logging.info("Botão ciclado")
       except:
        is_clickable = False
        logging.info("Botão não é clicável")
    
       logging.info(f"Botão de salvar é clicável? {is_clickable}")
    
     #Limpa o campo novamente para o próximo caso de teste
       input.send_keys(Keys.COMMAND + "a")
       input.send_keys(Keys.DELETE)
    
       return is_clickable
    
    def test_button_click(self):
        """
        Insere a senha válida e clica no botão 'Salvar'.
        Valida se o container de sucesso aparece e registra a URL atual.
        """
        passwpord_input = self.wait.until(EC.visibility_of_element_located(self.input_password))
        passwpord_input.send_keys(self.password)
        button_element =self.wait.until(EC.element_to_be_clickable(self.button))
        logging.info("Botão 'Salvar' clicável")
        button_element.click()

        logging.info("Senha válida e botão clicado")
        self.wait.until(EC.visibility_of_element_located(self.container))
        logging.info("Container do sucesso apareceu")


    def test_password_validation_and_save(self):
      """Valida se a senha foi salva exibindo apenas '*' na tela."""
      wait_dedicado = WebDriverWait(self.driver, 45)
      try:
           
        wait_dedicado.until(EC.text_to_be_present_in_element(self.success_field, "*"),
        "Tempo limite excedido: O texto da máscara ('*') não foi renderizado após salvar a senha.")
        logging.info("✅ Senha salva com sucesso — sequência de '*' exibida corretamente.")
        
      except TimeoutException as e:
        # Trata a falha de sincronização.
        logging.error(f"❌ Falha de Sincronização: Tempo esgotado. {e.msg}")
        raise AssertionError("Teste falhou: O indicador de sucesso (máscara) não ficou visível a tempo.")
