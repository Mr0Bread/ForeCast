import mysql.connector


class MySQLClient:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.database_connection = self.connect_to_database()
        self.cursor = self.database_connection.cursor()

    def connect_to_database(self):
        database_connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            database=self.database
        )
        return database_connection

    def get_all_info_from_database(self):
        command = 'SELECT * FROM data_records'
        self.cursor.execute(command)
        records = self.cursor.fetchall()
        return records
