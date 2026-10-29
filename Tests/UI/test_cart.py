
import allure
import pytest

from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage


@allure.feature("Shopping Cart")
@allure.story("Add product to cart")
@allure.title("Adding a backpack updates the cart quantity")
@pytest.mark.regression
@pytest.mark.ui
def test_adding_backpack_updates_cart_quantity(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login()

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"

    inventory_page.add_backpack_to_cart()

    assert inventory_page.cart_count() == "1"
