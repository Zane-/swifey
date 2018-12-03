import unittest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )

    # def test_search_in_python_org(self):
    #     driver = self.driver
    #     driver.get("http://www.python.org")
    #     self.assertIn("Python", driver.title)
    #     print(driver.title)
        # elem = driver.find_element_by_name("q")
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        # assert "No results found." not in driver.page_source

    def test_login_button(self):
        try:
            driver = self.driver
            print("About to get driver")
            driver.get("http://web:8000/")
            print("Title of Website: ", driver.title)
        except Exception as e:
            print(e)
        # title = str(driver.title)
        # self.assertEqual('Swifey', title)
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
