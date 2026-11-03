import allure
import pytest

from Pages.inventory_page import InventoryPage


EXPECTED_NAMES_AZ = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]


@allure.feature("Inventory")
@allure.story("Product sorting")
@allure.title("Verify products can be sorted by name")
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "option, expected",
    [
        ("az", EXPECTED_NAMES_AZ),
        ("za", EXPECTED_NAMES_AZ[::-1]),
    ],
)
def test_sort_products_by_name(
    logged_in_inventory,
    option,
    expected,
):
    inventory = logged_in_inventory

    inventory.sort_products(option)

    assert inventory.product_names() == expected


@allure.feature("Inventory")
@allure.story("Product sorting")
@allure.title("Verify products can be sorted by price")
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "option",
    ["lohi", "hilo"],
)
def test_sort_products_by_price(
    logged_in_inventory,
    option,
):
    inventory = logged_in_inventory

    inventory.sort_products(option)

    prices = inventory.product_prices()

    assert len(prices) == 6

    if option == "lohi":
        assert prices == sorted(prices)
    else:
        assert prices == sorted(prices, reverse=True)