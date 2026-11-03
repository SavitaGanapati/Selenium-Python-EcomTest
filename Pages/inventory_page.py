
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from Pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    # Product details
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_CARDS = (By.CLASS_NAME, "inventory_item")

    # Add-to-cart controls
    ADD_TO_CART_BUTTONS = (
        By.CSS_SELECTOR,
        "button[id^='add-to-cart-']"
    )

    # Navigation controls
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def add_product_to_cart(self, product_id):
        locator = (
            By.ID,
            f"add-to-cart-{product_id}"
        )
        self.click(locator)
        return self

    def remove_product_from_cart(self, product_id):
        locator = (
            By.ID,
            f"remove-{product_id}"
        )
        self.click(locator)
        return self

    def add_backpack_to_cart(self):
        return self.add_product_to_cart(
            "sauce-labs-backpack"
        )

    def cart_count(self):
        if self.is_visible(self.CART_BADGE):
            return self.get_text(self.CART_BADGE)
        return "0"

    def open_cart(self):
        self.click(self.CART_LINK)
        return self

    def open_menu(self):
        self.click(self.MENU_BUTTON)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.LOGOUT_LINK
            ).is_displayed()
        )
        return self

    def logout(self):
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        return self

    def product_names(self):
        self.wait.until(
            lambda driver: len(
                driver.find_elements(*self.PRODUCT_NAMES)
            ) > 0
        )
        return [
            element.text
            for element in self.driver.find_elements(
                *self.PRODUCT_NAMES
            )
        ]

    def product_prices(self):
        return [
            float(element.text.replace("$", ""))
            for element in self.driver.find_elements(
                *self.PRODUCT_PRICES
            )
        ]

    def sort_products(self, option):
        dropdown = self.wait.until(
            lambda driver: driver.find_element(
                *self.SORT_DROPDOWN
            )
        )
        Select(dropdown).select_by_value(option)
        return self

    def product_count(self):
        return len(
            self.driver.find_elements(*self.PRODUCT_CARDS)
        )

    def add_to_cart_button_count(self):
        return len(
            self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        )

    def inventory_controls_visible(self):
        return (
            self.is_visible(self.SORT_DROPDOWN)
            and self.is_visible(self.CART_LINK)
        )
