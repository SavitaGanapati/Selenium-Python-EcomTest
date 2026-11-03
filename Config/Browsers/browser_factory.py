
from selenium import webdriver

from Config.config_loader import load_config


class BrowserFactory:
    """Create local or remote Selenium browser sessions."""

    @staticmethod
    def create(browser_name=None, headless=None):
        config = load_config()

        browser_name = (
            browser_name or config["browser"]
        ).lower()

        if headless is None:
            headless = config["headless"]

        window_size = config["window_size"]
        platform = config["platform"].lower()

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Disable Chrome password-manager prompts in the
            # isolated automated test browser session.
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            }

            options.add_experimental_option("prefs", prefs)

            # This path is specific to local Windows execution.
            if platform == "local":
                options.binary_location = (
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                )

            if headless:
                options.add_argument("--headless=new")

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()

            if headless:
                options.add_argument("-headless")

        elif browser_name == "edge":
            options = webdriver.EdgeOptions()

            if headless:
                options.add_argument("--headless=new")

        else:
            raise ValueError(
                f"Unsupported browser: {browser_name}. "
                "Choose chrome, firefox, or edge."
            )

        if browser_name in ("chrome", "edge"):
            options.add_argument(f"--window-size={window_size}")

        elif browser_name == "firefox":
            width, height = window_size.split(",")
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")

        if platform == "local":
            if browser_name == "chrome":
                return webdriver.Chrome(options=options)

            if browser_name == "firefox":
                return webdriver.Firefox(options=options)

            return webdriver.Edge(options=options)

        if platform in ("remote", "docker", "grid"):
            remote_url = config["remote_url"]

            if not remote_url:
                raise ValueError(
                    "remote_url must be configured for remote execution."
                )

            return webdriver.Remote(
                command_executor=remote_url,
                options=options,
            )

        raise ValueError(
            f"Unsupported platform: {platform}. "
            "Choose local, remote, docker, or grid."
        )
