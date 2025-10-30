from pages.home_page import HomePage
from api_utils import get_wishlist_products


def test_mobile_flows(driver):
    home_page = HomePage(driver)

    home_page.open_americanas()

    home_page.search_products_1()
    home_page.search_products_2()
    #home_page.validate_product_name(iphone)

