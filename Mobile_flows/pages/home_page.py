from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import logging


class HomePage(BasePage):
    def __init__(self, driver):
      super().__init__(driver)

    def open_americanas(self):
       logging.info("O aplicativo das Americanas foi aberto")