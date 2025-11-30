import unittest
from unittest.mock import MagicMock, call
from lumos import Lumos, ElementNotFoundError
from selenium.common.exceptions import TimeoutException

class TestLumos(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.lumos = Lumos(self.mock_driver)

    def test_find_element_success(self):
        # Setup mock to return a WebElement
        mock_element = MagicMock()
        self.mock_driver.execute_script.return_value = mock_element
        
        # Call
        el = self.lumos.find_element("host > root > target")
        
        # Verify
        self.assertEqual(el, mock_element)
        # Check if execute_script was called (exact arguments are complex to match due to JS string)
        self.mock_driver.execute_script.assert_called()

    def test_find_element_failure(self):
        # Setup mock to return None (element not found)
        self.mock_driver.execute_script.return_value = None
        
        # Call & Verify
        with self.assertRaises(ElementNotFoundError):
            self.lumos.find_element("host > root > target", timeout=0.1)

    def test_click_force_js(self):
        mock_element = MagicMock()
        self.mock_driver.execute_script.side_effect = [mock_element, None] # First for find, second for click
        
        self.lumos.click("host > btn", force_js=True)
        
        # Verify click script was called
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_element)

if __name__ == '__main__':
    unittest.main()
