from  pages.product_page import ProductPage
from  pages.zipcode_page import ZipCodePage
from  pages.poupup_page import CartPage
from  pages.checkout_page import CheckoutPage
from api_utils import get_wishlist_products
import pytest

products_api = get_wishlist_products()


@pytest.mark.parametrize("product", products_api)
def test_mobile_flow(driver, product):
    mobile_products = ProductPage(driver)
    mobile_zip_code = ZipCodePage(driver)
    mobile_cart = CartPage(driver)
    mobile_checkout = CheckoutPage(driver)
  
    product_name = product["Product"]
    product_price = product["Price"]
    product_zip_code = product["Zipcode"]
    product_estimate = product["delivery_estimate"]
    product_shipping = product["shipping_fee"]

    
    mobile_products.search_product(product_name)
    mobile_products.validate_name_price(product_name, product_price)
    mobile_zip_code.validate_zip_code(product_zip_code, product_estimate, product_shipping)
    mobile_zip_code.click_buy_now()
    mobile_cart.cart_poup_up(product_name,product_price)
    mobile_cart.validate_quantity_change()
    mobile_cart.click_checkout()
    mobile_cart.checkout_flow(product_name, product_zip_code, product_shipping,product_estimate)
    mobile_checkout.validate_totals_and_finish(product_price)