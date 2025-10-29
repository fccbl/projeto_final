from pages.home_page import HomePage

def test_mobile_flows(driver):
    home_page = HomePage(driver)

    home_page.open_americanas()