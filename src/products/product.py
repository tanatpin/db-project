class Product:
    def __init__(self, db):
        self.db = db
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS product_list (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                price DECIMAL NOT NULL,
                stock INTEGER NOT NULL CHECK(stock >= 0),
                supplier_id INTEGER
            );
        """)
    

    def NewProduct(self, product_name, category, price, stock, supplier_id=None):
        if not product_name or price < 0 or stock < 0:
            raise ValueError("Invalid product details. Ensure name is provided and values are non-negative.")

        self.db.execute("""
            INSERT INTO product_list (product_name, category, price, stock, supplier_id)
            VALUES (?, ?, ?, ?, ?)
        """, (product_name, category, price, stock, supplier_id))

        print("New product added successfully!")



    def SearchProduct(self, product_id):
        result = self.db.execute("SELECT * FROM product_list WHERE product_id = ?", (product_id,)).fetchone()

        if result:
            print(f"Product ID: {result[0]}, Name: {result[1]}, Category: {result[2]}, Price: {result[3]}, Stock: {result[4]}")
        else:
            print("Product not found.")



    def UpdateProduct(self, product_id, product_name=None, category=None, price=None, stock=None, supplier_id=None):
        existing_product = self.db.execute("SELECT * FROM product_list WHERE product_id = ?", (product_id,)).fetchone()

        if not existing_product:
            print("Product not found.")
            return

        updates = []
        values = []

        if product_name:
            updates.append("product_name = ?")
            values.append(product_name)

        if category:
            updates.append("category = ?")
            values.append(category)

        if price is not None:
            updates.append("price = ?")
            values.append(price)

        if stock is not None:
            updates.append("stock = ?")
            values.append(stock)

        if supplier_id is not None:
            updates.append("supplier_id = ?")
            values.append(supplier_id)

        values.append(product_id)

        self.db.execute(f"""
            UPDATE product_list
            SET {', '.join(updates)}
            WHERE product_id = ?
        """, values)

        print("Product updated successfully!")
