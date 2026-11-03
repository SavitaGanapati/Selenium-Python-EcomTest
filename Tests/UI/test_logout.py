import allure
import pytest

from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage


@allure.feature("Authentication")
@allure.story("Logout and session management")
@allure.title("Logout returns user to login page")
@pytest.mark.regression
@pytest.mark.ui
def test_logout_returns_to_login(driver):

    inventory = InventoryPage(driver)

    LoginPage(driver).open().login()

    assert inventory.title() == "Products"

    inventory.logout()

    login_page = LoginPage(driver)

    login_page.wait.until(
        lambda browser: browser.current_url.rstrip("/").endswith(
            "saucedemo.com"
        )
    )

    assert driver.find_element(
        *login_page.LOGIN_BUTTON
    ).is_displayed()

    assert driver.find_element(
        *login_page.USERNAME_INPUT
    ).is_displayed()


@allure.feature("Authentication")
@allure.story("Logout and session management")
@allure.title("Logged-out user cannot access inventory directly")
@pytest.mark.regression
@pytest.mark.ui
def test_logged_out_user_cannot_access_inventory(driver):

    inventory = InventoryPage(driver)

    LoginPage(driver).open().login()

    assert inventory.title() == "Products"

    inventory.logout()

    driver.get(
        "https://www.saucedemo.com/inventory.html"
    )

    login_page = LoginPage(driver)

    login_page.wait.until(
        lambda browser: "inventory.html" not in browser.current_url
    )

    assert "inventory.html" not in driver.current_url

    assert driver.find_element(
        *login_page.LOGIN_BUTTON
    ).is_displayed()