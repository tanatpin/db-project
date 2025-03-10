class CustomerTransaction:
    def __init__(self, db):
        self.db = db
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS customer_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                total_amount DECIMAL NOT NULL CHECK(total_amount >= 0),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customer_list(customer_id)
            );
        """)

    def NewTransaction(self, customer_id, total_amount):
        # Ensure customer exists
        customer = self.db.execute("SELECT * FROM customer_list WHERE customer_id = ?", (customer_id,)).fetchone()
        if not customer:
            print("Error: Customer does not exist.")
            return

        # Insert new transaction
        self.db.execute("""
            INSERT INTO customer_transactions (customer_id, total_amount)
            VALUES (?, ?)
        """, (customer_id, total_amount))

        print("Transaction recorded successfully!")


    def CustomerPurchase(self, customer_id):
        transactions = self.db.execute("""
            SELECT transaction_id, total_amount, transaction_date 
            FROM customer_transactions 
            WHERE customer_id = ? 
            ORDER BY transaction_date DESC
        """, (customer_id,)).fetchall()

        if transactions:
            print(f"Transaction History for Customer ID {customer_id}:")
            for txn in transactions:
                print(f"Transaction ID: {txn[0]}, Amount: {txn[1]}, Date: {txn[2]}")
        else:
            print("No transactions found for this customer.")
