from random import seed
from time import time
import argparse

from .driver import Driver
from .birthday import Birthday
from .login import Login


def get_args():
    # Get help description from file
    with open('help-description', 'r') as description_file:
        help_description = description_file.read()

    parser = argparse.ArgumentParser(description=help_description, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-b', '--birthday-wish', action='store_true',
                        help='Checks for birthdays today and sends birthday wishes')
    parser.add_argument('-m', '--send-message', help='Send a message to the specified person (--fb-name or --msg-name)')
    parser.add_argument('-n', '--fb-name',
                        help='Name of the Facebook friend to send a message to. If you want to send a message to a group conversation or to a person that isn\'t on your friend list use --msg-name instead')
    parser.add_argument('--msg-name',
                        help='Name of the group conversation or existing conversation. This checks the conversations to the left in "https://www.facebook.com/messages/"')
    parser.add_argument('--init-mysql',
                        help='Initializes the mysql database. Needs to be called before you can schedule any messages')

    return parser.parse_args()


def __main__():
    args = get_args()
    seed(time())

    Driver.check_if_installed()
    driver = Driver.init_driver()
    Login.login(driver)

    if args.birthday_wish:
        Birthday.wish_birthday(driver)

__main__()

