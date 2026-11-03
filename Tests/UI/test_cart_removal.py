
import allure
import pytest

from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage
from Pages.cart_page import CartPage



@allure.feature("Shopping Cart")
@allure.story("Remove products from cart")
@allure.title("Remove one product directly from the cart")
@pytest.mark.regression
@pytest.mark.ui
def test_remove_product_from_cart(logged_in_inventory):
    inventory = logged_in_inventory

    inventory.add_product_to_cart("sauce-labs-backpack")
    inventory.add_product_to_cart("sauce-labs-bike-light")
    inventory.open_cart()

    cart = CartPage(inventory.driver)
    cart.wait_for_item_count(2)
    assert cart.item_count() == 2
    assert "Sauce Labs Backpack" in cart.item_names()
    assert "Sauce Labs Bike Light" in cart.item_names()

    cart.remove_product("sauce-labs-bike-light")

    cart.wait_for_item_count(1)
    assert cart.item_count() == 1
    assert cart.item_names() == ["Sauce Labs Backpack"]


@allure.feature("Shopping Cart")
@allure.story("Proceed to checkout")
@allure.title("Proceed from cart to checkout information")
@pytest.mark.regression
@pytest.mark.ui
def test_proceed_to_checkout(logged_in_inventory):
    inventory = logged_in_inventory

    inventory.add_product_to_cart("sauce-labs-backpack")
    inventory.open_cart()

    cart = CartPage(inventory.driver)
    # Wait until the cart item is rendered.
    cart.wait_for_item_count(1)

    assert cart.item_count() == 1
    assert "Sauce Labs Backpack" in cart.item_names()

    cart.checkout()

    assert inventory.driver.current_url.endswith(
        "/checkout-step-one.html"
    )
