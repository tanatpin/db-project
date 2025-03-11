class CustomerTransaction:
    def __init__(self, db):
        self.db = db

    def NewTransaction(self, customer_id, total_amount, transaction_date):
        """
        Inserts a new customer transaction.
        """
        query = """
        INSERT INTO CustomerTransactions (customer_id, total_amount, transaction_date)
        VALUES (?, ?, ?)
        """
        self.db.execute_query(query, (customer_id, total_amount, transaction_date))
        print("Transaction added successfully.")

    def CustomerPurchase(self, customer_id):
        """
        Retrieves all transactions for a given customer.
        """
        query = """
        SELECT transaction_id, total_amount, transaction_date
        FROM CustomerTransactions
        WHERE customer_id = ?
        """
        results = self.db.fetch_all(query, (customer_id,))
        
        if results:
            print("\nCustomer Transactions:")
            for row in results:
                print(f"Transaction ID: {row[0]}, Total Amount: {row[1]}, Date: {row[2]}")
        else:
            print("No transactions found for this customer.")
