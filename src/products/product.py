class Product:
    def __init__(self, db):
        self.db = db

    def NewProduct(self, product_name, category, price, stock_quantity):
        query = """
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (product_name, category, price, stock_quantity))
        print("Product added successfully!")

    def SearchProduct(self, product_id):
        query = "SELECT * FROM products WHERE product_id = ?"
        result = self.db.fetch_query(query, (product_id,))
        if result:
            print(result)
        else:
            print("Product not found.")

    def UpdateProduct(self, product_id, price=None, stock_quantity=None):
        updates = []
        params = []

        if price:
            updates.append("price = ?")
            params.append(price)
        if stock_quantity:
            updates.append("stock_quantity = ?")
            params.append(stock_quantity)

        if updates:
            query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?"
            params.append(product_id)
            self.db.execute_query(query, tuple(params))
            print("Product updated successfully!")
        else:
            print("No updates were made.")
