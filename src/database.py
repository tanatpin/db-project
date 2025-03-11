import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        """Executes a query and commits changes for INSERT, UPDATE, DELETE"""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_query(self, query, params=()):
        """Executes a SELECT query and returns the results"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        """Closes the database connection"""
        self.connection.close()
