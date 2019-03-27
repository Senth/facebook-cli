from random import random
from time import sleep


def random_user_delay():
    """Delays the script by a random amount to make us pass for a human"""
    delay = random() * 10.0 + 3.0
    sleep(delay)
