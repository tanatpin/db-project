class ProductTransaction:
    def __init__(self, db):
        self.db = db

    def RecordProductPurchase(self, transaction_id, product_id, quantity, subtotal):
        """
        Records a new product purchase in the ProductTransactions table.
        """
        query = """
        INSERT INTO ProductTransactions (transaction_id, product_id, quantity, subtotal)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (transaction_id, product_id, quantity, subtotal))
        print("Product purchase recorded successfully.")

    def ProductPurchase(self, product_id):
        """
        Retrieves purchase history for a given product.
        """
        query = """
        SELECT pt.product_transaction_id, pt.transaction_id, c.customer_id, c.first_name, c.last_name, 
               pt.quantity, pt.subtotal, ct.transaction_date
        FROM ProductTransactions pt
        JOIN CustomerTransactions ct ON pt.transaction_id = ct.transaction_id
        JOIN CustomerList c ON ct.customer_id = c.customer_id
        WHERE pt.product_id = ?
        """
        results = self.db.fetch_all(query, (product_id,))
        
        if results:
            print("\nProduct Purchase History:")
            for row in results:
                customer_name = row[3] + " " + row[4] if row[3] else "Company"
                print(f"Transaction ID: {row[1]}, Customer: {customer_name}, Quantity: {row[5]}, Subtotal: {row[6]}, Date: {row[7]}")
        else:
            print("No purchase history found for this product.")
