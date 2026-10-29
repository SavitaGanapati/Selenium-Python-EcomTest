
import json
import os
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config():
    """Load framework settings and allow environment overrides."""
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}"
        )

    with CONFIG_PATH.open("r", encoding="utf-8-sig") as file:
        config = json.load(file)

    required_keys = {
        "browser",
        "platform",
        "remote_url",
        "headless",
        "implicit_wait",
        "explicit_wait",
        "window_size",
    }
    missing_keys = required_keys - config.keys()

    if missing_keys:
        raise ValueError(
            f"Missing configuration keys: {sorted(missing_keys)}"
        )

    # Environment variables override JSON settings when provided.
    if os.getenv("BROWSER"):
        config["browser"] = os.getenv("BROWSER")

    if os.getenv("PLATFORM"):
        config["platform"] = os.getenv("PLATFORM")

    if os.getenv("REMOTE_URL"):
        config["remote_url"] = os.getenv("REMOTE_URL")

    if os.getenv("HEADLESS") is not None:
        config["headless"] = (
            os.getenv("HEADLESS").lower() == "true"
        )

    if os.getenv("IMPLICIT_WAIT") is not None:
        config["implicit_wait"] = int(os.getenv("IMPLICIT_WAIT"))

    if os.getenv("EXPLICIT_WAIT") is not None:
        config["explicit_wait"] = int(os.getenv("EXPLICIT_WAIT"))

    return config
