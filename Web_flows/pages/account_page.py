from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import time

class MyAccountPage():
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.my_account_button = (By.CSS_SELECTOR, "span.ButtonLogin_myAccount__mte5i")
        self.email_validate = (By.CSS_SELECTOR, ".vtex-my-account-1-x-emailContainer > .vtex-my-account-1-x-dataEntryChildren")
        self.link_authentication = (By.CSS_SELECTOR, 'a.vtex-account_menu-link[href="#/authentication"]')
        self.set_password = (By.CSS_SELECTOR,"button.vtex-button[type='button'] > div.vtex-button__label")
        self.input_code = (By.XPATH, "//input[@type='text' and contains(@class,'vtex-styleguide-')]")
        self.input_password = (By.CSS_SELECTOR, "input[type='password']")
        self.button = (By.XPATH, "//button[./div[text()='Salvar senha']]")
        self.success_field = (By.CSS_SELECTOR,".pa6.flex-grow-1.vtex-my-authentication-1-x-box_content .vtex-my-authentication-1-x-maskedPassword_content")
        self.password = "Abcdef12"

    def account_button_click(self,email):
        self.wait.until(EC.element_to_be_clickable(self.my_account_button)).click()
        logging.info("Clique no botão minha conta")
        account_email=self.wait.until(EC.visibility_of_element_located(self.email_validate)).text.strip()
        assert account_email == email
        logging.info("Email do usuário validado")

    def go_to_set_password(self):
        self.wait.until(EC.element_to_be_clickable(self.link_authentication)).click()
        button= self.wait.until(EC.element_to_be_clickable(self.set_password))
        button.click()
        logging.info("Clique no botão 'Definir senha' realizado com sucesso.")

        
    
    def enter_access_code(self,code):
        input = self.wait.until(EC.visibility_of_element_located(self.input_code))
        input.send_keys(code)
        logging.info(f"Código inserido:{code}")
    

    def test_password(self, password):
    # Espera o campo de senha estar visível
       input = self.wait.until(EC.visibility_of_element_located(self.input_password))
    
    # 🔹 Limpa o campo de forma confiável antes de digitar
       input.send_keys(Keys.COMMAND + "a")  # Se
       input.send_keys(Keys.DELETE)         
    
    # Digita a nova senha
       input.send_keys(password)
       logging.info(f"Senha inserida: {password}")
       time.sleep(1.5)

    # Verifica se o botão está clicável
       try:
        button_element =self.wait.until(EC.element_to_be_clickable(self.button))
        is_clickable = True
        button_element.click()
        logging.info("Botão ciclado")
       except:
        is_clickable = False
        logging.info("Botão não é clicável")
    
       logging.info(f"Botão de salvar é clicável? {is_clickable}")
    
    # 🔹 Limpa o campo novamente para o próximo caso de teste
       input.send_keys(Keys.COMMAND + "a")
       input.send_keys(Keys.DELETE)
    
       return is_clickable
    
    def test_button_click(self):
        input = self.wait.until(EC.visibility_of_element_located(self.input_password))
        input.send_keys(self.password)
        button_element =self.wait.until(EC.element_to_be_clickable(self.button)).click()
        logging.info("Senha válida e botão clicado")


    def test_password_validation_and_save(self):
     logging.info("Esperando aparecer a sequência de asteriscos da senha salva...")

     element = self.wait.until(EC.visibility_of_element_located(self.success_field))

     validate = element.text.strip()
     logging.info(f"Texto encontrado: '{validate}'")

    # Validação: confirma que a sequência contém asteriscos
     assert "*" in validate, f"O campo não está mascarado corretamente: {validate}"

    logging.info("Senha salva confirmada — sequência de asteriscos exibida.")

