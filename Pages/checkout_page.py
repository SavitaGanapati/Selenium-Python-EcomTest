from decimal import Decimal

from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class CheckoutPage(BasePage):

    # Checkout information
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Checkout overview
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")

    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")

    FINISH_BUTTON = (By.ID, "finish")

    # Order confirmation
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")

    def enter_customer_information(
        self, first_name, last_name, postal_code
    ):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def item_names(self):
        return [
            item.text
            for item in self.driver.find_elements(*self.ITEM_NAMES)
        ]

    def item_prices(self):
        return [
            self._to_decimal(item.text)
            for item in self.driver.find_elements(*self.ITEM_PRICES)
        ]

    def item_quantities(self):
        return [
            int(item.text)
            for item in self.driver.find_elements(*self.ITEM_QUANTITIES)
        ]

    def subtotal(self):
        return self._to_decimal(self.get_text(self.SUBTOTAL))

    def tax(self):
        return self._to_decimal(self.get_text(self.TAX))

    def total(self):
        return self._to_decimal(self.get_text(self.TOTAL))

    @staticmethod
    def _to_decimal(value):
        amount = value.replace("$", "").split(":")[-1].strip()
        return Decimal(amount)

    def finish_order(self):
        self.click(self.FINISH_BUTTON)
        return self

    def confirmation_header(self):
        return self.get_text(self.COMPLETE_HEADER)

    def confirmation_message(self):
        return self.get_text(self.COMPLETE_TEXT)