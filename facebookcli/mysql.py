from getpass import getpass
from MySQLdb._exceptions import OperationalError
import MySQLdb

from .config import MYSQL_DB
from .config import MYSQL_USER
from .config import MYSQL_PASSWORD

class MySql:
    def __init__(self):
        self.connection = MySQLdb.connect(host='localhost', user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)

    def schedule_message(self, scheduled_date, name, message):
        """Add the message to the DB"""

        cursor = self.connection.cursor()

        sql = 'INSERT INTO `scheduled` (`scheduled`, `name`, `message`) ' + \
                'VALUES (' + str(scheduled_date) + ", '" + name + "', '" + message + "')"
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    @staticmethod
    def create_db():
        """Creates a database, empty tables, and a user with access rights to the DB"""
        root_password = getpass(prompt='Existing MySQL root password (for creating a new mysql DB): ')

        try:
            connection = MySQLdb.connect(host='localhost', user='root', passwd=root_password)
            cursor = connection.cursor()

            # Create DB
            cursor.execute('CREATE DATABASE IF NOT EXISTS ' + MYSQL_DB)
            print('Created DB: ' + MYSQL_DB)
            cursor.execute('USE ' + MYSQL_DB)
    
            # Create table
            scheduled_table = 'CREATE TABLE IF NOT EXISTS `' + MYSQL_DB + '`.`scheduled` ( `id` INT(9) UNSIGNED NOT NULL AUTO_INCREMENT , `scheduled` INT(9) NOT NULL , `name` VARCHAR(50) NOT NULL , `message` TEXT NOT NULL , `sent` INT(9) NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB'
            cursor.execute(scheduled_table)
            print('Created table: scheduled')

            # Grant access for the user specified in the config
            create_user = 'GRANT ALL PRIVILEGES ON ' + MYSQL_DB + '.* ' + \
            'to ' + MYSQL_USER + '@localhost ' + \
            "identified by '" + MYSQL_PASSWORD + "'"
            cursor.execute(create_user)
            print("Created user '" + MYSQL_USER + "' with access to DB")
            connection.commit()

        except OperationalError:
            print('Access denied, wrong password')
        
        finally:
            cursor.close()
