from random import randrange
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .config import BIRTHDAY_MESSAGES
from .config import BIRTHDAY_MESSAGES_DEFAULT
from .utils import random_user_delay


class Birthday:
    _BIRTHDAY_ARTICLE_TITLE = "Today's Birthdays"

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def wish_birthday(self):
        """Checks if there are any friends to post a birthday wish for"""
        self.driver.get("https://mbasic.facebook.com/events/birthdays/")
        random_user_delay()

        more_people_to_post_to = True

        try:
            print("Find people to post birthday wishes to")
            while more_people_to_post_to:
                more_people_to_post_to = self._wish_birthday_for_all()

        except NoSuchElementException as e:
            print("No more birthdays today")

    def _get_todays_birthdays_container(self) -> WebElement:
        article: WebElement = self.driver.find_element_by_tag_name("article")

        # Check if the article is today's birthdays
        header: WebElement = article.find_element_by_tag_name("h3")
        if header.text == "Today's Birthdays":
            return article
        else:
            raise NoSuchElementException()

    def _wish_birthday_for_all(self):
        todays_birthdays_container = self._get_todays_birthdays_container()

        people_elements_container: WebElement = (
            todays_birthdays_container.find_element_by_tag_name("ul")
        )
        people_elements = people_elements_container.find_elements_by_xpath("*")

        for person_element in people_elements:
            posted = Birthday._wish_birthday_for(person_element)
            if posted:
                return True

    @staticmethod
    def _wish_birthday_for(person_element: WebElement) -> bool:
        name_element = person_element.find_element_by_xpath("a/div/p")
        full_name = name_element.text
        print(f"\nFound person {full_name}")

        # Get birthday wish and post
        if full_name in BIRTHDAY_MESSAGES:
            message = Birthday._get_message(full_name)
            return Birthday._wish_birthday(person_element, message)
        else:
            print(f"Didn't find {full_name} in birthday messages")

        return False

    @staticmethod
    def _wish_birthday(person_element: WebElement, message: str) -> bool:
        """Post a birthday wish to the person if we haven't already done so"""
        try:
            # Get text box
            print("Get text box")
            textarea = person_element.find_element_by_tag_name("textarea")
            textarea.send_keys(message)
            random_user_delay()

            # Post
            print("Post message")
            post_button = person_element.find_element_by_xpath(
                './/input[@value="Post"]'
            )
            post_button.submit()
            print(message)
            random_user_delay()
            return True

        except (ElementNotInteractableException, ElementNotVisibleException):
            print("Already posted a wish")
            return False

    @staticmethod
    def _get_message(full_name: str) -> str:
        """Get the birthday wish/message for the specified friend"""

        message = BIRTHDAY_MESSAGES[full_name]

        print("Found message: " + message)

        # Replace with a default message
        if message in BIRTHDAY_MESSAGES_DEFAULT:
            print("Replace with a randomized default message")
            default_messages = BIRTHDAY_MESSAGES_DEFAULT[message]

            # Randomize message
            message = default_messages[randrange(len(default_messages))]

            # Replace $ with first name
            first_name = full_name.split(" ", maxsplit=1)[0]
            message = message.replace("$", first_name)

        return message
