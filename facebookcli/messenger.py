from selenium.common.exceptions import NoSuchElementException
from re import search

from .utils import random_user_delay


class Messenger:
    def __init__(self, driver):
        self.driver = driver

    def send_message(self, name, message):
        """Send a message to a friend or a group conversation

        :param name Full name of a Facebook friend or the name of the group conversation
        """

        # Search for existing conversations first
        conversation_url = self._find_conversation_url(name)

        # Search for Facebook friend with specified name
        if conversation_url is None:
            friend_uid = self._find_friend_id(name)
            conversation_url = 'https://mbasic.facebook.com/messages/read/?fbid=' + friend_uid + '&_rdr'

        if not conversation_url is None:
            self._send_message(conversation_url, message)
        else:
            print("Couldn't find a conversation or friend with the name " + name)

    def _send_message(self, conversation_url, message):
        self.driver.get(conversation_url)
        random_user_delay()

        textarea = self.driver.find_element_by_tag_name('textarea')
        textarea.send_keys(message)
        random_user_delay()

        send_button = self.driver.find_element_by_xpath('//input[@value="Send"]')
#         send_button.submit()
        print('Message sent.')

    def _find_conversation_url(self, name):
        """Searches for recent conversations which has the specified name

        :return url of the conversation, `None` if not found
        """

        self.driver.get('https://mbasic.facebook.com/messages/' +
                        '?ref_component=mbasic_home_header&ref_page=MMessagingThreadlistController&refid=11')
        random_user_delay()
        people_elements_search = '//td[@class="t bw bx"]/div/h3/a'
        page = 1

        while True:
            print("Searching for '" + name + "' conversation on page " + str(page))
            people_elements = self.driver.find_elements_by_xpath(people_elements_search)

            # Remove special case if we have unanswered messages
            if page == 1 and len(people_elements) == 0:
                people_elements_search = '//h3[@class="bw ba bx"]/a'
                continue

            for person_element in people_elements:
                found_person = person_element.text
                # Found conversation
                if name == found_person:
                    conversation_url = person_element.get_attribute('href')
                    print('Found conversation url: ' + conversation_url)
                    return conversation_url

            # Go to next page if it exists
            try:
                see_older_messages_element = self.driver.find_element_by_xpath('//div[@id="see_older_threads"]/a')
                url = see_older_messages_element.get_attribute('href')
                self.driver.get(url)
                random_user_delay()
                people_elements_search = '//h3[@class="bw ba bx"]/a'
                page += 1

            except NoSuchElementException:
                print("Didn't find existing conversation with name " + name)
                return None

    def _find_friend_id(self, full_name):
        """Find a Facebook's friend id

        :return uid of friend, `None` if not found
        """

        self.driver.get('https://mbasic.facebook.com/friends/center/friends/?mff_nav=1')
        random_user_delay()
        page = 0

        while True:
            print("Searching for '" + name + "' friend on page " + str(page))
            friend_elements = self.driver.find_elements_by_xpath('//a[@class="bq"]')
            for friend_element in friend_elements:
                name = friend_element.text

                # Get id from href url
                if name == full_name:
                    href = friend_element.get_attribute('href')
                    match = search('uid=(\d*)', href)
                    friend_uid = match.group(1)
                    print('Found uid: ' + friend_uid)
                    return friend_uid

            # Go to the next page if it exists
            try:
                self.driver.find_element_by_xpath('//div[@id="u_0_0"]')
                self.driver.get(
                    'https://mbasic.facebook.com/friends/center/friends/?ppk=' + str(page) + '&tid=u_0_0&bph=' + str(
                        page) + '#friends_center_main')
                random_user_delay()
                page += 1

            except NoSuchElementException:
                print("Didn't find friend " + full_name)
                return None


