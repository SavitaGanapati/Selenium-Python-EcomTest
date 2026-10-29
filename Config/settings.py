import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

USERNAME = os.getenv("TEST_USERNAME", "standard_user")
PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")
