from pages.home_url import HomePage
from pages.login_page import LoginPage
from pages.account_page import MyAccountPage
from conftest import load_csv_test_cases
import pytest

def test_web_flow(driver, temp_mail_url, base_url_americanas):
    #HomePage
    home_page = HomePage(driver)
    home_page.navigate(base_url_americanas)
    home_page.close_popup()
    home_page.login_page()  

    #LoginPage
    login_page = LoginPage(driver)
    login_page.open_temp_mail_tab(temp_mail_url)
    email_temporario = login_page.get_temp_email()
    login_page.return_to_login_tab()
    login_page.email_input(email_temporario)
    login_page.button_send_email()
    login_page.return_to_temp_mail_tab()
    code = login_page.get_access_code()
    login_page.return_to_login_tab_after_code()
    login_page.codigo_input_field(code)
    login_page.button_confirm_code()
    login_page.validate_homepage(base_url_americanas)
    assert login_page.validate_login(email_temporario)

    #MyAccountPage
    account_page = MyAccountPage(driver)
    account_page.account_button_click(email_temporario)
    account_page.go_to_set_password()
    account_page.enter_access_code(code)
  # Cenário de teste
    test_post = load_csv_test_cases("test_case.csv")
    for case in test_post:
        password = case["password"]
        description = case["description"]
        expected_clickable = case["button_clickable"] == "True"
    
        is_clickable = account_page.test_password(password)
        assert is_clickable == expected_clickable, (
        f"Regra de senha falhou: {description} | "
        f"Esperado que o botão fosse clicável: {expected_clickable}, mas foi: {is_clickable}")
    account_page.test_button_click()    
    account_page.test_password_validation_and_save()



 
    