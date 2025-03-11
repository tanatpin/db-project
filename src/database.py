import sqlite3

class Database:
    def __init__(self, db_name="company_database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Ensures all required tables exist in the database."""
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_type TEXT CHECK (customer_type IN ('Individual', 'Company')),
            first_name TEXT,
            last_name TEXT,
            company_name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            branch_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS customer_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            total_amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        CREATE TABLE IF NOT EXISTS product_transactions (
            product_transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES customer_transactions(transaction_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        CREATE TABLE IF NOT EXISTS branches (
            branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        );
        """)
        self.connection.commit()

    def execute_query(self, query, params=()):
        """Executes INSERT, UPDATE, DELETE queries."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_query(self, query, params=()):
        """Executes SELECT queries and returns the result."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        """Closes the database connection."""
        self.connection.close()
