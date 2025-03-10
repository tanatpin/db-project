class ProductTransaction:
    def __init__(self, db):
        self.db = db
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS product_transactions (
                product_transaction_id INTEGER PRIMARY KEY,
                transaction_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                subtotal DECIMAL NOT NULL CHECK(subtotal >= 0),
                FOREIGN KEY (transaction_id) REFERENCES customer_transactions(transaction_id),
                FOREIGN KEY (product_id) REFERENCES product_list(product_id)
            );
        """)

    
    # Record a product purchase
    def RecordProductPurchase(self, transaction_id, product_id, quantity):
        # Ensure transaction exists
        transaction = self.db.execute("SELECT * FROM customer_transactions WHERE transaction_id = ?", (transaction_id,)).fetchone()
        if not transaction:
            print("Error: Transaction does not exist.")
            return

        # Ensure product exists
        product = self.db.execute("SELECT price, stock_quantity FROM product_list WHERE product_id = ?", (product_id,)).fetchone()
        if not product:
            print("Error: Product does not exist.")
            return
        
        # Ensure sufficient stock
        price, stock = product
        if stock < quantity:
            print("Error: Not enough stock available.")
            return

        # Calculate subtotal
        subtotal = price * quantity

        # Insert new product transaction
        self.db.execute("""
            INSERT INTO product_transactions (transaction_id, product_id, quantity, subtotal)
            VALUES (?, ?, ?, ?)
        """, (transaction_id, product_id, quantity, subtotal))

        # Update product stock
        new_stock = stock - quantity
        self.db.execute("UPDATE product_list SET stock_quantity = ? WHERE product_id = ?", (new_stock, product_id))

        print("Product purchase recorded successfully!")


    # Retrieve a Product's Purchase History
    def ProductPurchase(self, product_id):
        transactions = self.db.execute("""
            SELECT pt.transaction_id, c.customer_id, c.first_name, c.last_name, pt.quantity, pt.subtotal, ct.transaction_date 
            FROM product_transactions pt
            JOIN customer_transactions ct ON pt.transaction_id = ct.transaction_id
            JOIN customer_list c ON ct.customer_id = c.customer_id
            WHERE pt.product_id = ?
            ORDER BY ct.transaction_date DESC
        """, (product_id,)).fetchall()

        if transactions:
            print(f"Purchase History for Product ID {product_id}:")
            for txn in transactions:
                print(f"Transaction ID: {txn[0]}, Customer: {txn[2]} {txn[3]} (ID: {txn[1]}), Quantity: {txn[4]}, Subtotal: {txn[5]}, Date: {txn[6]}")
        else:
            print("No purchases found for this product.")
