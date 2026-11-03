import allure
import pytest

from Pages.cart_page import CartPage
from Pages.checkout_page import CheckoutPage


def open_checkout(logged_in_inventory):
    inventory = logged_in_inventory

    inventory.add_product_to_cart("sauce-labs-backpack")
    inventory.open_cart()

    cart = CartPage(inventory.driver)
    cart.wait_for_item_count(1)

    assert cart.item_count() == 1
    assert "Sauce Labs Backpack" in cart.item_names()

    cart.checkout()

    checkout = CheckoutPage(inventory.driver)

    checkout.wait.until(
        lambda driver: driver.current_url.endswith(
            "/checkout-step-one.html"
        )
    )

    return checkout


@allure.feature("Checkout")
@allure.story("Required field validation")
@allure.title("Validate mandatory checkout information")
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_error",
    [
        ("", "Ganapati", "560061",
         "Error: First Name is required"),
        ("Savita", "", "560061",
         "Error: Last Name is required"),
        ("Savita", "Ganapati", "",
         "Error: Postal Code is required"),
    ],
)
def test_checkout_required_field_validation(
    logged_in_inventory,
    first_name,
    last_name,
    postal_code,
    expected_error,
):
    checkout = open_checkout(logged_in_inventory)

    checkout.enter_customer_information(
        first_name,
        last_name,
        postal_code,
    )

    checkout.continue_checkout()

    assert checkout.error_message() == expected_error


@allure.feature("Checkout")
@allure.story("Customer information")
@allure.title("Valid customer information advances to order overview")
@pytest.mark.regression
@pytest.mark.ui
def test_valid_checkout_information(logged_in_inventory):
    checkout = open_checkout(logged_in_inventory)

    checkout.enter_customer_information(
        "Savita",
        "Ganapati",
        "560061",
    )

    checkout.continue_checkout()

    checkout.wait.until(
        lambda driver: driver.current_url.endswith(
            "/checkout-step-two.html"
        )
    )

    assert checkout.item_names() == ["Sauce Labs Backpack"]


@allure.feature("Checkout")
@allure.story("Order overview")
@allure.title("Validate products and order price calculations")
@pytest.mark.regression
@pytest.mark.ui
def test_checkout_order_overview(logged_in_inventory):
    checkout = open_checkout(logged_in_inventory)

    checkout.enter_customer_information(
        "Savita",
        "Ganapati",
        "560061",
    )

    checkout.continue_checkout()

    checkout.wait.until(
        lambda driver: driver.current_url.endswith(
            "/checkout-step-two.html"
        )
    )

    assert checkout.item_count() == 1
    assert checkout.item_names() == ["Sauce Labs Backpack"]
    assert checkout.item_quantities() == [1]

    item_total = sum(checkout.item_prices())

    assert checkout.subtotal() == item_total
    assert checkout.total() == (
        checkout.subtotal() + checkout.tax()
    )


@allure.feature("Checkout")
@allure.story("Order completion")
@allure.title("Complete order and verify confirmation")
@pytest.mark.regression
@pytest.mark.ui
def test_complete_checkout_order(logged_in_inventory):
    checkout = open_checkout(logged_in_inventory)

    checkout.enter_customer_information(
        "Savita",
        "Ganapati",
        "560061",
    )

    checkout.continue_checkout()

    checkout.wait.until(
        lambda driver: driver.current_url.endswith(
            "/checkout-step-two.html"
        )
    )

    assert checkout.item_names() == ["Sauce Labs Backpack"]

    checkout.finish_order()

    checkout.wait.until(
        lambda driver: driver.current_url.endswith(
            "/checkout-complete.html"
        )
    )

    assert checkout.confirmation_header() == (
        "Thank you for your order!"
    )