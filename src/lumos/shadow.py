from typing import List, Union, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .exceptions import ElementNotFoundError

class Lumos:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_element(self, css_path: Union[str, List[str]], timeout: int = 10) -> WebElement:
        """
        Finds an element inside nested shadow DOMs using a 'host > nested > target' syntax.
        
        :param css_path: String path separated by ' > ' or a list of selectors.
                         Example: "user-profile > settings-card > button.save"
        :param timeout: Time to wait for the element to appear.
        """
        if isinstance(css_path, str):
            selectors = [s.strip() for s in css_path.split(">")]
        else:
            selectors = css_path

        # The Robust JS Script
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

    def click(self, css_path: Union[str, List[str]], timeout: int = 10, force_js: bool = False):
        """
        Helper to find and click in one step.
        
        :param css_path: Path to the element.
        :param timeout: Wait timeout.
        :param force_js: If True, uses JavaScript to click instead of Selenium's .click().
        """
        element = self.find_element(css_path, timeout)
        if force_js:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            element.click()

    def find_by_text(self, text_content: str, timeout: int = 10) -> WebElement:
        """
        Recursively scans ALL shadow roots to find an element containing specific text.
        Returns the element itself.
        """
        js_finder = """
        function searchShadow(root, text) {
            // Get all elements in this root
            let all = root.querySelectorAll('*');
            for (let el of all) {
                // Check if element has the text and is visible (basic check)
                // We check if it has direct text content match or contains it
                if (el.innerText && el.innerText.includes(text)) {
                     // If it's a leaf node or close to it, it's a better match
                     // But for now, let's return the first match that has no children or children don't have the text
                     // A simple heuristic: if it has no children, it's a match.
                     if (el.children.length === 0) return [el];
                }
                
                // Recursion: Check if this element has a shadow root
                if (el.shadowRoot) {
                    let found = searchShadow(el.shadowRoot, text);
                    if (found) {
                        return found; 
                    }
                }
            }
            return null;
        }
        
        // Wrapper to handle the search
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
