from pages.home_page import HomePage
from pages.apple_watch import Second_Product


def test_mobile_flows(driver):
    home_page = HomePage(driver)
    apple_watch = Second_Product(driver)

    #home_page.search_products_1()
     #home_page.search_products_2()
    # home_page.search_products_3()
   
   
    apple_watch.search_products_2()
    apple_watch.validade_name_price()
    apple_watch.validade_zip_code()
    apple_watch.buy_product()
    apple_watch.cart_poup_up()
