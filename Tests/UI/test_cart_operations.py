
import allure
import pytest

from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage
from Pages.cart_page import CartPage


@allure.feature("Shopping Cart")
@allure.story("Add and remove products")
@allure.title("Add two products and remove one from inventory")
@pytest.mark.regression
@pytest.mark.ui
def test_add_two_products_and_remove_one(
    logged_in_inventory
):
    inventory = logged_in_inventory

    assert inventory.title() == "Products"

    inventory.add_product_to_cart("sauce-labs-backpack")
    inventory.add_product_to_cart("sauce-labs-bike-light")

    assert inventory.cart_count() == "2"

    inventory.remove_product_from_cart("sauce-labs-bike-light")

    assert inventory.cart_count() == "1"

    inventory.open_cart()

    cart = CartPage(inventory.driver)

    assert cart.title() == "Your Cart"
    assert cart.item_count() == 1


@allure.feature("Shopping Cart")
@allure.story("Continue shopping")
@allure.title("Continue shopping after opening the cart")
@pytest.mark.regression
@pytest.mark.ui
def test_continue_shopping(logged_in_inventory):
    inventory = logged_in_inventory

    inventory.add_product_to_cart("sauce-labs-backpack")
    inventory.open_cart()

    cart = CartPage(inventory.driver)
    assert cart.title() == "Your Cart"

    cart.continue_shopping()

    assert inventory.title() == "Products"
