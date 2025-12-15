from typing import List, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .exceptions import ElementNotFoundError


class Lumos:
    """A robust Shadow DOM traverser for Selenium."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize Lumos with a Selenium WebDriver.

        Args:
            driver: A Selenium WebDriver instance.
        """
        self.driver = driver

    def find_element(self, css_path: Union[str, List[str]], timeout: int = 10) -> WebElement:
        """
        Finds an element inside nested shadow DOMs using a 'host > nested > target' syntax.

        Args:
            css_path: String path separated by ' > ' or a list of selectors.
                      Example: "user-profile > settings-card > button.save"
            timeout: Time in seconds to wait for the element to appear.

        Returns:
            WebElement: The found element.

        Raises:
            ElementNotFoundError: If element is not found within timeout.

        Example:
            >>> lumos = Lumos(driver)
            >>> btn = lumos.find_element("user-card > button.edit")
            >>> btn.click()
        """
        if isinstance(css_path, str):
            selectors = [s.strip() for s in css_path.split(">")]
        else:
            selectors = css_path

        script = """
        const selectors = arguments[0];
        let root = document;
        let el = null;
        
        for (let i = 0; i < selectors.length; i++) {
            el = root.querySelector(selectors[i]);
            if (!el) return null;
            
            if (i < selectors.length - 1) {
                if (!el.shadowRoot) return null;
                root = el.shadowRoot;
            }
        }
        return el;
        """

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(lambda d: d.execute_script(script, selectors))
            if not element:
                raise TimeoutException()
            return element
        except TimeoutException:
            path_str = " > ".join(selectors)
            raise ElementNotFoundError(f"Lumos could not find element at path: {path_str}")

    def find_elements(self, css_path: Union[str, List[str]], timeout: int = 10) -> List[WebElement]:
        """
        Finds ALL elements matching the path inside nested shadow DOMs.

        Args:
            css_path: String path separated by ' > ' or a list of selectors.
                      The last selector can match multiple elements.
                      Example: "user-list > user-card > button.delete"
            timeout: Time in seconds to wait for at least one element to appear.

        Returns:
            List[WebElement]: List of matching elements (may be empty after timeout).

        Example:
            >>> lumos = Lumos(driver)
            >>> buttons = lumos.find_elements("app-root > nav-menu > button")
            >>> for btn in buttons:
            ...     print(btn.text)
        """
        if isinstance(css_path, str):
            selectors = [s.strip() for s in css_path.split(">")]
        else:
            selectors = list(css_path)

        script = """
        const selectors = arguments[0];
        let root = document;
        let el = null;
        
        // Navigate to the parent shadow root
        for (let i = 0; i < selectors.length - 1; i++) {
            el = root.querySelector(selectors[i]);
            if (!el) return [];
            
            if (!el.shadowRoot) return [];
            root = el.shadowRoot;
        }
        
        // Find all matching elements with the last selector
        const lastSelector = selectors[selectors.length - 1];
        return Array.from(root.querySelectorAll(lastSelector));
        """

        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(lambda d: d.execute_script(script, selectors))
            return elements if elements else []
        except TimeoutException:
            return []

    def click(self, css_path: Union[str, List[str]], timeout: int = 10, force_js: bool = False) -> None:
        """
        Helper to find and click an element in one step.

        Args:
            css_path: Path to the element.
            timeout: Wait timeout in seconds.
            force_js: If True, uses JavaScript to click instead of Selenium's .click().
        """
        element = self.find_element(css_path, timeout)
        if force_js:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            element.click()

    def find_by_text(self, text_content: str, timeout: int = 10) -> WebElement:
        """
        Recursively scans ALL shadow roots to find an element containing specific text.

        Args:
            text_content: The text to search for (case-sensitive).
            timeout: Time in seconds to wait for the element.

        Returns:
            WebElement: The first matching element found.

        Raises:
            ElementNotFoundError: If no element with the text is found.
        """
        js_finder = """
        function searchShadow(root, text) {
            let all = root.querySelectorAll('*');
            for (let el of all) {
                if (el.innerText && el.innerText.includes(text)) {
                     if (el.children.length === 0) return [el];
                }
                
                if (el.shadowRoot) {
                    let found = searchShadow(el.shadowRoot, text);
                    if (found) {
                        return found; 
                    }
                }
            }
            return null;
        }
        
        let found = searchShadow(document, arguments[0]);
        return found ? found[0] : null;
        """

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(lambda d: d.execute_script(js_finder, text_content))
            if not element:
                raise TimeoutException()
            return element
        except TimeoutException:
            raise ElementNotFoundError(f"Lumos could not find element containing text: '{text_content}'")
