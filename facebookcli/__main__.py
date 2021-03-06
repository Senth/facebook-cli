from random import seed
from time import time
from sys import exit
from sys import argv
from os import path
import argparse

from .driver import Driver
from .birthday import Birthday
from .login import Login
from .messenger import Messenger
from .mysql import MySql
from .schedule import Schedule


def get_args():
    # Get help description from file
    help_file = path.join(path.dirname(path.abspath(__file__)), "help-description")
    with open(help_file, "r") as description_file:
        help_description = description_file.read()

    parser = argparse.ArgumentParser(
        description=help_description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-b",
        "--birthday-wish",
        action="store_true",
        help="Checks for birthdays today and sends birthday wishes",
    )
    parser.add_argument(
        "-m",
        "--send-message",
        metavar="MESSAGE",
        help="Send a message to a friend or existing group conversation (--name)",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name of the friend, group conversation, or existing conversation. "
        + "This first looks after existing conversations to the left in "
        + '"https://www.facebook.com/messages/", if not found there it will look '
        + "for a Facebook friends with the specified name",
    )
    parser.add_argument(
        "--create-mysql-db",
        action="store_true",
        help="Initializes the MySQL with a new database. Needs to be called before you can schedule any messages",
    )
    parser.add_argument(
        "-s",
        "--schedule-message",
        metavar="MESSAGE",
        help="Schedule a message for a friend, requires --name, --date, and --time",
    )
    parser.add_argument(
        "-r",
        "--run-scheduled-messages",
        action="store_true",
        help="Checks if there are any scheduled messages that should be sent and sends them",
    )
    parser.add_argument(
        "-d",
        "--date",
        help="Date to send the scheduled message on in the format YYYY-MM-DD",
    )
    parser.add_argument(
        "-t",
        "--time",
        help="Time to send the scheduled message on in the format HH:MM (24-hours)",
    )

    # Display help if no arguments was passed
    if len(argv) < 2:
        parser.print_help()
        exit(0)

    return parser.parse_args()


def main():
    args = get_args()
    seed(time())

    Driver.check_if_installed()
    driver = Driver.init_driver()

    # Birthday
    if args.birthday_wish:
        login = Login(driver)
        login.login()
        birthday = Birthday(driver)
        birthday.wish_birthday()
    # Send Message
    elif args.send_message:
        # Check so a name has been supplied
        if args.name is None:
            print("Please supply the message with a --name NAME")
            exit(1)

        login = Login(driver)
        login.login()
        messenger = Messenger(driver)
        messenger.send_message(args.name, args.send_message)
    # Create MySQL DB
    elif args.create_mysql_db:
        MySql.create_db()
    # Schedule a message
    elif args.schedule_message:
        # Check for missing args
        if args.date is None:
            print("Please supply the message with a --date DATE")
            exit(1)
        elif args.time is None:
            print("Please supply the message with a --time TIME")
            exit(1)
        elif args.name is None:
            print("Please supply the message with a --name NAME")
            exit(1)

        schedule = Schedule()
        schedule.schedule_message(
            args.date, args.time, args.name, args.schedule_message
        )
    elif args.run_scheduled_messages:
        schedule = Schedule()
        schedule.run_scheduled_messages(driver)

    driver.quit()


if __name__ == "__main__":
    main()
