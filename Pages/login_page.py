from selenium.webdriver.common.by import By

from Config.settings import BASE_URL, USERNAME, PASSWORD
from Pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(BASE_URL)
        return self

    def login(self, username=None, password=None):
        self.type_text(
            self.USERNAME_INPUT,
            username if username is not None else USERNAME
        )
        self.type_text(
            self.PASSWORD_INPUT,
            password if password is not None else PASSWORD
        )
        self.click(self.LOGIN_BUTTON)
        return self

    def error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
