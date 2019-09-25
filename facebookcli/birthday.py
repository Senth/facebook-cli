from random import randrange
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException

from .config import BIRTHDAY_MESSAGES
from .config import BIRTHDAY_MESSAGES_DEFAULT
from .utils import random_user_delay


class Birthday:
    _BIRTHDAY_ARTICLE_TITLE = "Today's Birthdays"
    _BIRTHDAY_PEOPLE_CSS_CLASS = 'bk bv'
    _NAME_CSS_CLASS = 'bx by bs'

    def __init__(self, driver):
        self.driver = driver

    def wish_birthday(self):
        """Checks if there are any friends to post a birthday wish for"""
        self.driver.get('https://mbasic.facebook.com/events/birthdays/')
        random_user_delay()

        more_people_to_post_to = True

        try:
            print('Find people to post birthday wishes to')
            while more_people_to_post_to:
                birthday_article_element = self.driver.find_element_by_xpath(
                    '//div[@title ="' + Birthday._BIRTHDAY_ARTICLE_TITLE + '"]')
                birthday_people_element = birthday_article_element.find_elements_by_xpath(
                    './/div[@class ="' + Birthday._BIRTHDAY_PEOPLE_CSS_CLASS + '"]')

                more_people_to_post_to = Birthday._wish_birthday_for_all(birthday_people_element)

        except NoSuchElementException:
            print('No more birthdays today')

    @staticmethod
    def _wish_birthday_for_all(people_elements):
        """Iterate through all people """
        for person_element in people_elements:
            # Get name
            name_element = person_element.find_element_by_xpath(".//div[@class = '" + Birthday._NAME_CSS_CLASS + "']")
            full_name = name_element.text
            print('Found person ' + full_name)

            # Get birthday wish and post
            if full_name in BIRTHDAY_MESSAGES:
                message = Birthday._get_message(full_name)
                posted = Birthday._wish_birthday(person_element, message)

                # Return because page has been updated and people_elements is now a stale element
                if posted:
                    return True
            else:
                print('Didn\'t find ' + full_name + ' in birthday messages')

        return False

    @staticmethod
    def _wish_birthday(person_element, message):
        """Post a birthday wish to the person if we haven't already done so"""
        try:
            # Get text box
            print('Get text box')
            textarea = person_element.find_element_by_tag_name('textarea')
            textarea.send_keys(message)
            random_user_delay()

            # Post
            print('Post message')
            post_button = person_element.find_element_by_xpath('.//input[@value="Post"]')
            post_button.submit()
            print(message)
            random_user_delay()
            return True

        except (ElementNotInteractableException, ElementNotVisibleException):
            # print('Already posted a wish for ' + full_name)
            return False

    @staticmethod
    def _get_message(full_name):
        """Get the birthday wish/message for the specified friend"""

        message = BIRTHDAY_MESSAGES[full_name]

        print('Found message: ' + message)

        # Replace with a default message
        if message in BIRTHDAY_MESSAGES_DEFAULT:
            print('Replace with a randomized default message')
            default_messages = BIRTHDAY_MESSAGES_DEFAULT[message]

            # Randomize message
            message = default_messages[randrange(len(default_messages))]

            # Replace $ with first name
            first_name = full_name.split(' ', maxsplit=1)[0]
            message = message.replace('$', first_name)

        return message
