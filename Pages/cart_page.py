from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class CartPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def item_count(self):
        return len(
            self.driver.find_elements(*self.CART_ITEMS)
        )

    def wait_for_item_count(self, expected_count):
        """Wait until the cart contains the expected number of items."""
        self.wait.until(
            lambda driver: len(
                driver.find_elements(*self.CART_ITEMS)
            ) == expected_count
        )
        return self
    def item_names(self):
        return [
            element.text
            for element in self.driver.find_elements(
                *self.CART_ITEM_NAMES
            )
        ]

    def remove_product(self, product_id):
        locator = (
            By.ID,
            f"remove-{product_id}"
        )
        self.click(locator)
        return self

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
