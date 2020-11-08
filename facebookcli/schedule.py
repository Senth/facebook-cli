from re import fullmatch
from sys import exit
from datetime import datetime

from .mysql import MySql
from .messenger import Messenger
from .login import Login


class Schedule:
    def __init__(self):
        self.mysql = MySql()

    def schedule_message(self, date, time, name, message):
        """Convert date and time into unix epoch and store it in the DB"""

        # Check for correct date string
        match = fullmatch("2[01][0-9][0-9]-[01][0-9]-[0-3][0-9]", date)
        if not match:
            print("Invalid date syntax '" + date + "' please use YYYY-MM-DD")
            exit(0)

        # Check for correct time string
        match = fullmatch("[0-2][0-9]:[0-5][0-9]", time)
        if not match:
            print("Invalid time syntax '" + time + "' please use HH:MM")
            exit(0)

        # Convert date & time -> python datetime object
        datetime_object = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")

        # Convert datetime to unix epoch
        unix_epoch_time = int(datetime_object.timestamp())

        self.mysql.schedule_message(unix_epoch_time, name, message)
        print("Scheduled message")

    def run_scheduled_messages(self, driver):
        # Get all scheduled messages
        messages_to_send = self.mysql.get_messages_to_send()
        print("Found " + str(len(messages_to_send)) + " to send")

        if len(messages_to_send) > 0:
            Login.login(driver)
            messenger = Messenger(driver)

        for message_to_send in messages_to_send:
            id = message_to_send[0]
            name = message_to_send[1]
            message = message_to_send[2]

            messenger.send_message(name, message)

            self.mysql.set_message_as_sent(id)

        print("Sent all scheduled messages")
