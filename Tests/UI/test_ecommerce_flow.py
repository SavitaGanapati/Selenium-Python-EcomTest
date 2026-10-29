
import allure
import pytest

from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage


@allure.epic("E-commerce Test Automation")
@allure.feature("Shopping Cart")
@allure.story("Authenticated user adds a product to the cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("User can log in and add a backpack to the cart")
@pytest.mark.smoke
@pytest.mark.ui
def test_user_can_login_and_add_product_to_cart(driver):
    """Verify that a user can log in and add a product to the cart."""

    # Arrange: open the demo application
    login_page = LoginPage(driver)
    login_page.open()

    # Act: log in
    login_page.login()

    # Assert: inventory page is displayed
    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"

    # Act: add a backpack to the cart
    inventory_page.add_backpack_to_cart()

    # Assert: cart badge shows one item
    assert inventory_page.cart_count() == "1"
