from selenium import webdriver
from os.path import exists
from sys import exit

from .config import CHROME_DRIVER_BIN


class Driver:
    @staticmethod
    def check_if_installed():
        """Check if the driver has been installed (and is located at specified location). Quits the script if not"""
        if not exists(CHROME_DRIVER_BIN):
            print('--------------')
            print('ERROR: Could not find chromedriver at (' + CHROME_DRIVER_BIN + ')')
            print('Please install it through your distributions package manager and set the correct path in config.py')
            exit(0)

    @staticmethod
    def init_driver():
        """Initializes chromedriver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--lang=en-us')

        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(CHROME_DRIVER_BIN, chrome_options=chrome_options)
        return driver


