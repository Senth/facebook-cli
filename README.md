# facebookcli
Command Line Interface for various FB actions

- **Birthday Wishes:** Automatically post birthday wishes to your friends on their wall (through messenger coming soon)
- **Messages:** Send a message through FB Messenger
- **Scheduled Messages:** Schedule a message and send it to FB Messenger (comes with web interface)
- **Run Scheduled Messages:** Activate this to run the scheduled messages

## Installation

### 1. Install from pip repository to your user repository
```
pip3 install --user facebookcli
```

### 2. Configure facebookcli
1. Run `facebookcli` once. There should now be a message saying: "This seems like it's the first time you run this program. [...]" You should see the location of where the `config.py` file should be located. There is also an example file `config.example.py` in the same directory.
2. Go to the configuration folder. (usually `cd ~/.local/config/facebookcli` in linux)
3. Run: `cp config.example.py config.py`
4. Now configure `config.py`; you don't have to create a MySQL user or database. Just enter the username and password you would like to use.
5. Run: `chmod 600 config.py` to make sure only you have access to the config file since your Facebook password is stored in plain text.

### 3. Create MySQL database (optional)
In order to schedule and run scheduled messages you have to use a MySQL database.

To create a database simply run `facebookcli --create-mysql-db` and follow the instructions on screen.

### 4. Schedule with cron (optional)
#### Post birthdays
This scripts randomizes the time you post your birthdays between 10:00 and 13:00 (10am and 1pm)
```
0	10	*	*	*	python -c 'import random; import time; time.sleep(random.random() * 10800)' && LC_CTYPE=en_US.UTF-8 /usr/bin/python3 ~/.local/bin/facebookcli -b
```
The `LC_CTYPE=en_US.UTF-8` is needed if messages or friend names has non ascii names like åäö. If not supplied the script will fail.

#### Send scheduled messages
To be able to send scheduled messages you have to run `facebookcli -r` every now and then. It's up to you how often you want to run your script; this script run every other minute. Note that it will only login to Facebook if there are any messages to send.
```
*/2	*	*	*	*	LC_CTYPE=en_US.UTF-8 /usr/bin/python3 ~/.local/bin/facebookcli -r
```
The `LC_CTYPE=en_US.UTF-8` is needed if messages or friend names has non ascii names like åäö. If not supplied the script will fail.

## Command usage
```
usage: facebookcli [-h] [-b] [-m MESSAGE] [-n NAME] [--create-mysql-db]
                   [-s MESSAGE] [-r] [-d DATE] [-t TIME]

optional arguments:
  -h, --help            show this help message and exit
  -b, --birthday-wish   Checks for birthdays today and sends birthday wishes
  -m MESSAGE, --send-message MESSAGE
                        Send a message to a friend or existing group
                        conversation (--name)
  -n NAME, --name NAME  Name of the friend, group conversation, or existing
                        conversation. This first looks after existing
                        conversations to the left in
                        "https://www.facebook.com/messages/", if not found
                        there it will look for a Facebook friends with the
                        specified name
  --create-mysql-db     Initializes the MySQL with a new database. Needs to be
                        called before you can schedule any messages
  -s MESSAGE, --schedule-message MESSAGE
                        Schedule a message for a friend, requires --name,
                        --date, and --time
  -r, --run-scheduled-messages
                        Checks if there are any scheduled messages that should
                        be sent and sends them
  -d DATE, --date DATE  Date to send the scheduled message on in the format
                        YYYY-MM-DD
  -t TIME, --time TIME  Time to send the scheduled message on in the format
                        HH:MM (24-hours)
```

## Examples
### Post birthday messages on FB
`facebookcli -b`

### Send message to a friend or group conversation
Of course sending a message this way isn't really efficient. But you can.
```
facebookcli -m "Hello! You ready for tomorrow's party? :)" -n "Emma Daisy"
facebookcli -m "Hey Everyone! Last call to speak up before we finalize the time for next meetup." -n "Board Members"
```

### Schedule messages
Scheduled messages does not run automatically. You have to setup a cron or call `facebookcli -r` to actually send messages.
```
facebookcli -s "Hello! You ready for tomorrow's party? :)" -n "Emma Daisy" -d "2020-12-30" -t "18:00"
facebookcli -s "Hey Everyone! Last call to speak up before we finalize the time for next meetup." -n "Board Members" -d "2020-02-14" -t "13:00"
```


## Future features
- Simple website to add, remove, and show all scheduled messages.
