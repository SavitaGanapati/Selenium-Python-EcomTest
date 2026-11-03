import allure
import pytest

from Pages.inventory_page import InventoryPage


EXPECTED_PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]


@allure.feature("Inventory")
@allure.story("Inventory display")
@allure.title("Verify inventory products and shopping controls")
@pytest.mark.regression
@pytest.mark.ui
def test_inventory_display(logged_in_inventory):

    inventory = logged_in_inventory

    assert inventory.title() == "Products"

    assert inventory.product_count() == 6

    assert inventory.product_names() == EXPECTED_PRODUCTS

    prices = inventory.product_prices()

    assert len(prices) == 6
    assert all(price > 0 for price in prices)

    assert inventory.add_to_cart_button_count() == 6

    assert inventory.inventory_controls_visible()