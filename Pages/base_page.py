
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Config.config_loader import load_config
from Utils.Logs.logger import logger


class BasePage:
    """Shared Selenium interactions for all page objects."""

    def __init__(self, driver, timeout=None):
        self.driver = driver
        config = load_config()
        self.timeout = (
            config["explicit_wait"] if timeout is None else timeout
        )
        self.wait = WebDriverWait(driver, self.timeout)

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        logger.info("Clicked element: %s", locator)

    def type_text(self, locator, text, clear=True):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        if clear:
            element.clear()
        element.send_keys(text)
        logger.info("Entered text into element: %s", locator)

    def get_text(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def is_visible(self, locator):
        try:
            self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            logger.warning("Element was not visible: %s", locator)
            return False

    def get_page_title(self):
        return self.driver.title

    def get_page_url(self):
        return self.driver.current_url
