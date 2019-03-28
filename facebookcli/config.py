from os import path
from os import system
import sys
import site
import importlib.util

CONFIG_RELATIVE_DIR = path.join('config', 'facebookcli')
CONFIG_RELATIVE_FILE = path.join(CONFIG_RELATIVE_DIR, 'config.py')
CONFIG_RELATIVE_EXAMPLE = path.join(CONFIG_RELATIVE_DIR, 'config.example.py')

# Search for config file in sys path
sys_config = path.join(sys.prefix, CONFIG_RELATIVE_FILE)
user_config = path.join(site.getuserbase(), CONFIG_RELATIVE_FILE)
config_file = ''
if path.exists(sys_config):
    config_file = sys_config
elif path.exists(user_config):
    config_file = user_config
# User hasn't configured the program yet
else:
    sys_config_example = path.join(sys.prefix, CONFIG_RELATIVE_EXAMPLE)
    user_config_example = path.join(site.getuserbase(), CONFIG_RELATIVE_EXAMPLE)
    if path.exists(sys_config_example):
        config_example_file = sys_config_example
        config_file = path.join(sys.prefix, CONFIG_RELATIVE_FILE)
    elif path.exists(user_config_example):
        config_example_file = user_config_example
        config_file = path.join(site.getuserbase(), CONFIG_RELATIVE_FILE)
    # Couldn't find the example file
    else:
        print("Error: no configuration found. It should be here: '" + user_config + "'")
        print('run: locate ' + CONFIG_RELATIVE_EXAMPLE)
        print('This should help you find the current config location.')
        print('Otherwise you can download the config.py from https://github.com/Senth/facebook-cli/tree/master/config and place it in the correct location')
        sys.exit(0)

    print("This seems like it's the first time you run this program.")
    print("For this program to work properly you have to configure it by editing '" + config_file + "'.")
    print("In the same folder there's an example file 'config.example.py' you can copy to 'config.py'.")
    sys.exit(0)

spec = importlib.util.spec_from_file_location("config", user_config)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

def print_missing(variable_name):
    print('Missing ' + variable_name + ' variable in config file: ' + config_file)
    print('Please add it to you config.py again to continue')
    sys.exit(0)

try:
    FB_EMAIL = config.FB_EMAIL
except AttributeError:
    print_missing('FB_EMAIL')

try:
    FB_PASSWORD = config.FB_PASSWORD
except AttributeError:
    print_missing('FB_PASSWORD')

try:
    CHROME_DRIVER_BIN = config.CHROME_DRIVER_BIN
except AttributeError:
    print_missing('CHROME_DRIVER_BIN')

try:
    MYSQL_DB = config.MYSQL_DB
except AttributeError:
    print_missing('MYSQL_DB')

try:
    MYSQL_USER = config.MYSQL_USER
except AttributeError:
    print_missing('MYSQL_USER')

try:
    MYSQL_PASSWORD = config.MYSQL_PASSWORD
except AttributeError:
    print_missing('MYSQL_PASSWORD')

try:
    BIRTHDAY_MESSAGES_DEFAULT = config.BIRTHDAY_MESSAGES_DEFAULT
except AttributeError:
    print_missing('BIRTHDAY_MESSAGES_DEFAULT')

try:
    BIRTHDAY_MESSAGES = config.BIRTHDAY_MESSAGES
except AttributeError:
    print_missing('BIRTHDAY_MESSAGES')


