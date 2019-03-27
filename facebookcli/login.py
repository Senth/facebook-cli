from .config import FB_EMAIL, FB_PASSWORD
from .utils import random_user_delay

class Login:
    @staticmethod
    def login(driver):
        """Tries to login the user"""

        # open facebook.com using get() method
        driver.get('https://mbasic.facebook.com/')
        random_user_delay()

        element = driver.find_elements_by_xpath('//*[@id="m_login_email"]')
        element[0].send_keys(FB_EMAIL)
        print("Username Entered")

        element = driver.find_element_by_xpath('//*[@name="pass"]')
        element.send_keys(FB_PASSWORD)
        print("Password Entered")

        # logging in
        log_in = driver.find_elements_by_xpath('//*[@name="login"]')
        log_in[0].click()
        print("Login Successfull")
        random_user_delay()
