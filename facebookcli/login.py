from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .config import FB_EMAIL, FB_PASSWORD
from .utils import random_user_delay


class Login:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self._driver = driver

    def login(self):
        """Tries to login the user"""

        # open facebook.com using get() method
        self._driver.get("https://mbasic.facebook.com/")
        random_user_delay()

        # First try
        self._try_login()

        # Should be an error first time, try to login again
        if self._driver.title.startswith("Error"):
            login_button: WebElement = self._find_login_button()
            login_button.click()
            random_user_delay()

            # Second try
            self._try_login()

        print("Login Successfull")

    def _try_login(self):
        element: WebDriver = self._driver.find_elements_by_xpath(
            '//*[@id="m_login_email"]'
        )
        element[0].send_keys(FB_EMAIL)
        print("Username Entered")

        element = self._driver.find_element_by_xpath('//*[@name="pass"]')
        element.send_keys(FB_PASSWORD)
        print("Password Entered")

        # logging in
        log_in = self._driver.find_elements_by_xpath('//*[@name="login"]')
        log_in[0].click()
        random_user_delay()

    def _find_login_button(self) -> WebElement:
        return self._driver.find_element_by_xpath(
            './/a[contains(@href, "https://mbasic.facebook.com/login.php")]'
        )
