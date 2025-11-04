from pages.iphone_17 import First_Product
from pages.apple_watch import Second_Product
from pages.macbook_air import Third_Product


def test_mobile_flows(driver):
    iphone_17 = First_Product(driver)
    apple_watch = Second_Product(driver)
    macbook_air = Third_Product(driver)


    iphone_17.search_products_1()
    iphone_17.validate_name_price()
    iphone_17.validate_zip_code()
    iphone_17.buy_product()
    iphone_17.cart_poupup()
    iphone_17.click_checkout()
    iphone_17.page_car()
   
    #SecondProduct
    # apple_watch.search_products_2()
    # apple_watch.validade_name_price()
    # apple_watch.validade_zip_code()
    # apple_watch.buy_product()
    # apple_watch.cart_poup_up()



   #ThirdProduct
    # macbook_air.search_products_3()
    # macbook_air.validate_name_price()
    # macbook_air.validate_zip_code()
    # macbook_air.buy_product()
    # macbook_air.cart_poup_up()
    # macbook_air.validate_quantity_change()
    # macbook_air.click_checkout()
    # macbook_air.page_car()