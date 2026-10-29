
from pathlib import Path

import pytest
import pytest_html

from Config.config_loader import load_config
from Config.Browsers.browser_factory import BrowserFactory
from Utils.Logs.logger import logger


@pytest.fixture
def driver():
    config = load_config()
    browser = None

    try:
        logger.info("Starting browser: %s", config["browser"])
        browser = BrowserFactory.create(
            browser_name=config["browser"],
            headless=config["headless"],
        )
        browser.implicitly_wait(config["implicit_wait"])
        yield browser

    finally:
        if browser is not None:
            logger.info("Closing browser: %s", config["browser"])
            browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        logger.warning("No browser fixture available for failure screenshot")
        return

    screenshot_dir = Path("artifacts") / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(
        char if char.isalnum() or char in "-_"
        else "_"
        for char in item.nodeid
    )
    screenshot_path = screenshot_dir / f"{safe_name}.png"

    try:
        if browser.save_screenshot(str(screenshot_path)):
            logger.error("Failure screenshot saved: %s", screenshot_path)

            extras = getattr(report, "extras", [])
            extras.append(
                pytest_html.extras.image(
                    browser.get_screenshot_as_base64(),
                    name="Failure screenshot",
                    mime_type="image/png",
                )
            )
            report.extras = extras

    except Exception:
        logger.exception("Failed to capture or attach failure screenshot")
