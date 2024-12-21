import mysql.connector
from mysql.connector import MySQLConnection

class MySQLWrapper:
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.conn = None
        self.cursor = None
        self.transaction_started = False

        self.__init()

    def connect(self) -> None:
        self.conn = mysql.connector.connect(
            host=self.mysql_host,
            database=self.mysql_db,
            user=self.mysql_user,
            password=self.mysql_password
        )

    def __init(self) -> None:
        if self.conn is None:
            self.connect()

        if self.cursor is None:
            self.cursor = self.conn.cursor(dictionary=True)

    def start_transaction(self) -> None:
        if self.conn is None or self.cursor is None:
            self.__init()

        if not self.transaction_started:
            self.conn.start_transaction()
            self.transaction_started = True

    def rollback(self) -> None:
        if self.transaction_started:
            self.conn.rollback()
            self.transaction_started = False

    def commit(self) -> None:
        if self.transaction_started:
            self.conn.commit()
            self.transaction_started = False

    def destroy(self) -> None:
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def get_connection(self) -> MySQLConnection:
        return self.conn