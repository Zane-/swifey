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

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def test_title(self):
        driver = self.driver
        driver.get("http://web:8000/")
        title = str(driver.title)
        self.assertEqual('Swifey', title)

    def test_login_button(self):
        driver = self.driver
        driver.get("http://web:8000/")
        driver.find_element_by_name('login').click()
        heading = driver.find_element_by_tag_name('h3')
        self.assertEqual('Login', heading.text)
    
    def test_signup(self):
        firstName = "Mike"
        lastName = "Bob"
        email = "mikebob@gmail.com"
        university = "UVA"
        password = "password"
        driver = self.driver
        driver.get("http://web:8000/")
        driver.find_element_by_name("signup").click()
        first_name = driver.find_element_by_id("id_first_name")
        first_name.send_keys(firstName)
        last_name = driver.find_element_by_id("id_last_name")
        last_name.send_keys(lastName)
        email_id = driver.find_element_by_id("id_email")
        email_id.send_keys(email)
        university_id = driver.find_element_by_id("id_university")
        university_id.send_keys(university)
        password_id = driver.find_element_by_id("id_password")
        password_id.send_keys(password)
        confirm_password = driver.find_element_by_id("id_confirm_password")
        confirm_password.send_keys(password)
        driver.find_element_by_id("submit-id-submit").click()
        assert "Did not successfully sign up" not in driver.page_source

    def test_login(self):
        driver = self.driver
        driver.get("http://web:8000/")
        driver.find_element_by_name("login").click()
        driver.find_element_by_name("email").send_keys("test@gmail.com")
        driver.find_element_by_name("password").send_keys("password")
        driver.find_element_by_name("submit").click() 
        assert "Did not successfully login" not in driver.page_source
        self.assertEqual("You have successfully logged in.", driver.page_source)

    def test_logout(self):
        driver = self.driver
        driver.get("http://web:8000/")
        driver.find_element_by_name("logout").click()
        assert "Did not successfully logout" not in driver.page_source
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
