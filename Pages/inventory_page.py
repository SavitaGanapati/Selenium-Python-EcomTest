from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    ADD_BACKPACK_BUTTON = (
        By.ID, "add-to-cart-sauce-labs-backpack"
    )
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BUTTON)
        return self

    def cart_count(self):
        return self.get_text(self.CART_BADGE)

    def open_cart(self):
        self.click(self.CART_LINK)
