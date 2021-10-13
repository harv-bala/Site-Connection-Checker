import sqlite3
from sqlite3 import Error
from pathlib import Path

class DBHelper():
    def __init__(self) -> None:
        # Set the location of the database, as well as the filename. The Path class from pathlib automatically
        # corrects a path based on the OS. On Windows, this would change the '/' to a '\'.
        self.db_path = Path('db/websiteDB.db')

        # Set the SQL pattern for creation of the 'websites' table. Status is set as an integer because
        # SQLite does not have a Boolean data type, so 0 and 1 act as True and False.
        # 'domain' refers to the domain name of the website, e.g. https://www.google.com
        # 'status' refers to whether the website is live or down. 0 = Live, 1 = Down
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

    def create_connection(self):
        connection = None
        try:
            # Creating a connection to the database, passing in the path attribute
            connection = sqlite3.connect(str(self.db_path))
            print('Connection to DB established')
        except Error as e:
            print(f'The following error occurred: {e}')
        return connection

    def execute_query(self, query):
        # Establish connection to DB
        connection = self.create_connection()
        # The cursor allows traversal over the records in the DB. It is used to execute SQL queries on the DB.
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            # Commit (save) the changes made
            connection.commit()
            print('Query executed')
        except Error as e:
            print(f'The following error occurred: {e}')

    def execute_read_query(self, query):
        # Establish connection to DB
        connection = self.create_connection()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            # fetchall() returns all of the rows that matched the query we executed with the cursor
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f'The following error occurred: {e}')