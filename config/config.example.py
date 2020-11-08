FB_EMAIL = "your@email.com"
FB_PASSWORD = "your-fb-password"
# Be sure to install the chromedriver through your distribution's package manager, such as apt, yum, or emerge.
CHROME_DRIVER_BIN = "/usr/bin/chromedriver"

# These are default messages that can be reused.
# $ is replaced with the first name of the person
BIRTHDAY_MESSAGES_DEFAULT = {
    "english": [
        "Happy Birthday, $! :D",
        "Happy Birthday, $! :) Hope you'll have a wonderful day!",
    ],
    "swedish": [
        "Grattis på födelsedagen $! :D",
        "Grattis på födelsedagen $! :D Hoppas du får en fin dag! :)",
    ],
}

# Add all people that you want to wish birthday for in here.
# To use a default birthday message, simply set the message to the identifier from BIRTHDAY_MESSAGE_DEFAULT.
# E.g. as in the example below, Sara Doe will get a randomized english message, whereas Andreas Svensson will get
# a randomized swedish message
BIRTHDAY_MESSAGES = {
    "John Doe": "Happy birthday, John! :D Hope you'll have a great day :)",
    "Sara Doe": "english",
    "Andreas Svensson": "swedish",
}
