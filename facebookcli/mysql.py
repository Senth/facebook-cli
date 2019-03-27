from getpass import getpass
from MySQLdb._exceptions import OperationalError
import MySQLdb

from .config import MYSQL_DB
from .config import MYSQL_USER
from .config import MYSQL_PASSWORD

class MySql:
    def __init__(self):
        print('testing')

    @staticmethod
    def create_db():
        root_password = getpass(prompt='Existing MySQL root password (for creating a new mysql DB): ')

        try:
            connection = MySQLdb.connect(host='localhost', user='root', passwd=root_password)
            cursor = connection.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS ' + MYSQL_DB)
            cursor.execute('USE ' + MYSQL_DB)
     
            scheduled_table = 'CREATE TABLE IF NOT EXISTS `facebookcli`.`scheduled` ( `id` INT(9) UNSIGNED NOT NULL AUTO_INCREMENT , `scheduled` INT(9) NOT NULL , `name` VARCHAR(50) NOT NULL , `message` TEXT NOT NULL , `sent` INT(9) NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB'
            cursor.execute(scheduled_table)
        except OperationalError:
            print('Access denied, wrong password')
