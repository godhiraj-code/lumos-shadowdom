import unittest
from unittest.mock import MagicMock
from lumos import Lumos, ElementNotFoundError


class TestLumos(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_driver = MagicMock()
        self.lumos = Lumos(self.mock_driver)

    def test_find_element_success(self) -> None:
        """Test that find_element returns an element when found."""
        mock_element = MagicMock()
        self.mock_driver.execute_script.return_value = mock_element

        el = self.lumos.find_element("host > root > target")

        self.assertEqual(el, mock_element)
        self.mock_driver.execute_script.assert_called()

    def test_find_element_failure(self) -> None:
        """Test that find_element raises ElementNotFoundError when not found."""
        self.mock_driver.execute_script.return_value = None

        with self.assertRaises(ElementNotFoundError):
            self.lumos.find_element("host > root > target", timeout=0.1)

    def test_find_elements_success(self) -> None:
        """Test that find_elements returns a list of elements."""
        mock_elements = [MagicMock(), MagicMock(), MagicMock()]
        self.mock_driver.execute_script.return_value = mock_elements

        elements = self.lumos.find_elements("host > button")

        self.assertEqual(len(elements), 3)
        self.assertEqual(elements, mock_elements)

    def test_find_elements_empty(self) -> None:
        """Test that find_elements returns empty list when no elements found."""
        self.mock_driver.execute_script.return_value = None

        elements = self.lumos.find_elements("host > button", timeout=0.1)

        self.assertEqual(elements, [])

    def test_find_elements_with_list_path(self) -> None:
        """Test that find_elements works with list path input."""
        mock_elements = [MagicMock()]
        self.mock_driver.execute_script.return_value = mock_elements

        elements = self.lumos.find_elements(["host", "button"])

        self.assertEqual(elements, mock_elements)

    def test_click_force_js(self) -> None:
        """Test that click with force_js uses JavaScript click."""
        mock_element = MagicMock()
        self.mock_driver.execute_script.side_effect = [mock_element, None]

        self.lumos.click("host > btn", force_js=True)

        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_element)

    def test_click_native(self) -> None:
        """Test that click without force_js uses native click."""
        mock_element = MagicMock()
        self.mock_driver.execute_script.return_value = mock_element

        self.lumos.click("host > btn", force_js=False)

        mock_element.click.assert_called_once()

    def test_find_by_text_success(self) -> None:
        """Test that find_by_text returns element when found."""
        mock_element = MagicMock()
        self.mock_driver.execute_script.return_value = mock_element

        el = self.lumos.find_by_text("Submit")

        self.assertEqual(el, mock_element)

    def test_find_by_text_failure(self) -> None:
        """Test that find_by_text raises ElementNotFoundError when not found."""
        self.mock_driver.execute_script.return_value = None

        with self.assertRaises(ElementNotFoundError):
            self.lumos.find_by_text("NonExistentText", timeout=0.1)


if __name__ == '__main__':
    unittest.main()

