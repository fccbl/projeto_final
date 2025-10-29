from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging


class HomePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.popup_close_button = (By.CSS_SELECTOR, "div.ins-element-content")
        self.login_button = (By.CSS_SELECTOR, "a[href='/login']")

    def navigate(self, url):
        """Abre a página inicial na URL fornecida e limpa cookies"""
        self.driver.get(url)
 
    
    def close_popup(self):
        """Fecha o popup de anúncio se ele estiver visível."""
        try:
          self.wait.until(EC.visibility_of_element_located(self.popup_close_button)).click()
          logging.info("Popup fechado com sucesso!")
        except:
          logging.info("Nenhum poupup foi exibido")

    def login_page(self):
        """Clica no botão de login para navegar para a tela de autenticação."""
        try:
         self.wait.until(EC.visibility_of_element_located(self.login_button))
         logging.info("Botão de login visível na tela.")

         self.wait.until(EC.element_to_be_clickable(self.login_button)).click()
         logging.info("Clique no botão de login realizado com sucesso!")

        except: 
            logging.error(f"Erro ao clicar no botão de login")


