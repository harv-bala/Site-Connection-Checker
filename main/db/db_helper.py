import sqlite3
from sqlite3 import Error
from pathlib import Path

class DBHelper():
    def __init__(self) -> None:
        # Set the location of the database, as well as the filename. The Path class from pathlib automatically
        # corrects a path based on the OS. On Windows, this would change the '/' to a '\'.
        self.db_path = Path('db/websiteDB.db')

        # Set the SQL pattern for creation of the 'websites' table. Status is set as an integer because
        # SQLite does not have a Boolean data type, so 1 and 0 act as True and False.
        # 'domain' refers to the domain name of the website, e.g. https://www.google.com
        # 'status' refers to whether the website is live or down. 0 = Down, 1 = Live
        self.create_table_sql = '''CREATE TABLE IF NOT EXISTS websites (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    domain TEXT NOT NULL,
                                    status INTEGER NOT NULL
                                );'''

        # General SQL pattern for inserting a record. Using .format(), the gaps '{}' can be filled in
        # with whatever values are needed.
        self.insert_record_sql = '''INSERT INTO
                                        websites (domain, status)
                                    VALUES
                                        ("{}", {});
                                    '''

        # Read record by its domain name, used when getting a website's status
        self.read_record_sql = 'SELECT * FROM websites WHERE domain="{}"'

        self.read_all_sql = 'SELECT * FROM websites'

        # If a website's status changes, this SQL will change the status for the
        # domain name given
        self.update_record_sql = '''UPDATE websites
                                        SET status={}
                                    WHERE domain="{}"
                                    '''

        # Removes a record based on matching domain name
        self.delete_record_sql = 'DELETE FROM websites WHERE domain="{}"'

        self.create_table()

    def create_connection(self):
        connection = None
        try:
            # Creating a connection to the database, passing in the path attribute
            # The Path object much be cast to a strig when passed to the connect function
            connection = sqlite3.connect(str(self.db_path))
        except Error as e:
            print(f'The following error occurred: {e}')
        return connection

    def create_table(self):
        connection = self.create_connection()
        # The cursor allows iteration over the records in the database, and handles the execution
        # of any SQL
        cursor = connection.cursor()
        try:
            cursor.execute(self.create_table_sql)
            # After making changes, they are committed (saved)
            connection.commit()
        except Error as e:
            print(f'The following error occurred: {e}')

    # ---------- CREATE ----------
    def create_record(self, domain):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            # .format() is used to insert the arguments into the pre-set SQL pattern
            cursor.execute(self.insert_record_sql.format(domain, 1))
            connection.commit()
        except Error as e:
            print(f'The following error occurred: {e}')

    # ---------- READ ----------
    def read_record(self, domain):
        connection = self.create_connection()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(self.read_record_sql.format(domain))
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f'The following error occurred: {e}')

    def read_all_records(self):
        connection = self.create_connection()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(self.read_all_sql)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f'The following error occurred: {e}')

    # ---------- UPDATE ----------
    def update_record(self, domain, status):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(self.update_record_sql.format(status, domain))
            connection.commit()
        except Error as e:
            print(f'The following error occurred: {e}')

    # ---------- DELETE ----------
    def delete_record(self, domain):
        connection = self.create_connection()
        cursor = connection.cursor()
        if self.read_record(domain):
            try:
                cursor.execute(self.delete_record_sql.format(domain))
                connection.commit()
            except Error as e:
                print(f'The following error occurred: {e}')
        else:
            print(f"The website '{domain}' does not exist")