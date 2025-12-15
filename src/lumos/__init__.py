from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .shadow import Lumos
from .exceptions import LumosException, ShadowRootNotFoundError, ElementNotFoundError

__all__ = ["Lumos", "LumosException", "ShadowRootNotFoundError", "ElementNotFoundError"]


def find_shadow(self: WebDriver, css_path: str, timeout: int = 10) -> WebElement:
    """
    Monkey-patched method to find an element in Shadow DOM.

    Args:
        css_path: Path using '>' separator. Example: "host > nested > target"
        timeout: Seconds to wait for the element.

    Returns:
        WebElement: The found element.

    Usage:
        driver.find_shadow("host > nested > target")
    """
    lumos = Lumos(self)
    return lumos.find_element(css_path, timeout)


def find_all_shadow(self: WebDriver, css_path: str, timeout: int = 10) -> List[WebElement]:
    """
    Monkey-patched method to find ALL elements matching a path in Shadow DOM.

    Args:
        css_path: Path using '>' separator. Example: "host > nested > button"
        timeout: Seconds to wait for elements.

    Returns:
        List[WebElement]: List of matching elements.

    Usage:
        buttons = driver.find_all_shadow("app-root > nav > button")
    """
    lumos = Lumos(self)
    return lumos.find_elements(css_path, timeout)


def find_shadow_text(self: WebDriver, text: str, timeout: int = 10) -> WebElement:
    """
    Monkey-patched method to find an element by text in Shadow DOM.

    Args:
        text: The text to search for.
        timeout: Seconds to wait for the element.

    Returns:
        WebElement: The found element.

    Usage:
        driver.find_shadow_text("Submit")
    """
    lumos = Lumos(self)
    return lumos.find_by_text(text, timeout)


# Extend the standard WebDriver class dynamically
WebDriver.find_shadow = find_shadow  # type: ignore[attr-defined]
WebDriver.find_all_shadow = find_all_shadow  # type: ignore[attr-defined]
WebDriver.find_shadow_text = find_shadow_text  # type: ignore[attr-defined]

