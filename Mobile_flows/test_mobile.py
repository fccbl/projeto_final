from pages.home_page import HomePage
from pages.prod2_validate import Validade_Product_2


def test_mobile_flows(driver):
    home_page = HomePage(driver)
    prod2_validate = Validade_Product_2(driver)

    #home_page.search_products_1()
     #home_page.search_products_2()
    # home_page.search_products_3()
   
   
    prod2_validate.search_products_2()
    prod2_validate.validade_name_price()
    prod2_validate.validade_zip_code()
    
