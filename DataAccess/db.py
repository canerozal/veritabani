import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = None
        self.database = "degirmencilik_db"

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print("Veritabanı bağlantı hatası:", e)
            return None