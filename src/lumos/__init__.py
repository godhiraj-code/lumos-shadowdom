from selenium.webdriver.remote.webdriver import WebDriver
from .shadow import Lumos
from .exceptions import LumosException, ShadowRootNotFoundError, ElementNotFoundError

__all__ = ["Lumos", "LumosException", "ShadowRootNotFoundError", "ElementNotFoundError"]

def find_shadow(self, css_path, timeout=10):
    """
    Monkey-patched method to find elements in Shadow DOM.
    Usage: driver.find_shadow("host > nested > target")
    """
    l = Lumos(self)
    return l.find_element(css_path, timeout)

def find_shadow_text(self, text, timeout=10):
    """
    Monkey-patched method to find elements by text in Shadow DOM.
    Usage: driver.find_shadow_text("Submit")
    """
    l = Lumos(self)
    return l.find_by_text(text, timeout)

# Extend the standard WebDriver class dynamically
WebDriver.find_shadow = find_shadow
WebDriver.find_shadow_text = find_shadow_text
