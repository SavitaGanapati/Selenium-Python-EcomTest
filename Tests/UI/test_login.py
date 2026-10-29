
import allure
import pytest

from Pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("Invalid login")
@allure.title("Invalid credentials display an error message")
@pytest.mark.regression
@pytest.mark.ui
def test_invalid_login_displays_error(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(
        username="invalid_user",
        password="wrong_password",
    )

    error = login_page.error_message()

    assert "Username and password do not match" in error
