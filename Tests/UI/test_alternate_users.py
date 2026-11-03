import time

import allure
import pytest

from Config.settings import PASSWORD
from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage
from Utils.Logs.logger import logger


INVENTORY_URL = "/inventory.html"


def verify_inventory_access(driver):
    inventory = InventoryPage(driver)

    inventory.wait.until(
        lambda browser: browser.current_url.endswith(INVENTORY_URL)
    )

    assert inventory.title() == "Products"
    assert inventory.product_count() == 6

    return inventory


@allure.feature("Authentication")
@allure.story("Alternate demo users")
@allure.title("Standard user can access inventory")
@pytest.mark.regression
@pytest.mark.ui
def test_standard_user_access(driver):

    LoginPage(driver).open().login(
        username="standard_user",
        password=PASSWORD,
    )

    inventory = verify_inventory_access(driver)

    assert inventory.product_names()

    logger.info("Standard user successfully accessed inventory.")


@allure.feature("Authentication")
@allure.story("Alternate demo users")
@allure.title("Problem user login and inventory behaviour")
@pytest.mark.regression
@pytest.mark.ui
def test_problem_user_behaviour(driver):

    LoginPage(driver).open().login(
        username="problem_user",
        password=PASSWORD,
    )

    inventory = verify_inventory_access(driver)

    image_elements = driver.find_elements(
        "css selector",
        ".inventory_item_img img",
    )

    image_sources = [
        image.get_attribute("src")
        for image in image_elements
    ]

    assert len(image_sources) == 6
    assert all(image_sources)

    logger.info(
        "Problem user inventory image sources: %s",
        image_sources,
    )


@allure.feature("Authentication")
@allure.story("Alternate demo users")
@allure.title("Performance glitch user can access inventory")
@pytest.mark.regression
@pytest.mark.ui
def test_performance_glitch_user_behaviour(driver):

    login_page = LoginPage(driver).open()

    start_time = time.perf_counter()

    login_page.login(
        username="performance_glitch_user",
        password=PASSWORD,
    )

    inventory = verify_inventory_access(driver)

    elapsed_seconds = time.perf_counter() - start_time

    assert inventory.product_names()

    logger.info(
        "Performance glitch user login-to-inventory duration: %.2f seconds",
        elapsed_seconds,
    )


@allure.feature("Authentication")
@allure.story("Alternate demo users")
@allure.title("Locked out user is denied access")
@pytest.mark.regression
@pytest.mark.ui
def test_locked_out_user(driver):

    LoginPage(driver).open().login(
        username="locked_out_user",
        password=PASSWORD,
    )

    login_page = LoginPage(driver)

    assert login_page.error_message() == (
        "Epic sadface: Sorry, this user has been locked out."
    )

    assert INVENTORY_URL not in driver.current_url

    logger.info("Locked out user was correctly denied access.")