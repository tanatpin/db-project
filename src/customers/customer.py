class Customer:
    def __init__(self, db):
        self.db = db

    def NewCustomer(self, customer_type, first_name, last_name, company_name, email, phone, branch_id):
        query = """
        INSERT INTO customers (customer_type, first_name, last_name, company_name, email, phone, branch_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (customer_type, first_name, last_name, company_name, email, phone, branch_id))
        print("Customer added successfully!")

    def SearchCustomer(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = ? OR first_name LIKE ? OR last_name LIKE ? OR company_name LIKE ? OR email LIKE ?"

        searchWildCard = f"%{customer_id}%"

        result = self.db.fetch_query(query, (customer_id, searchWildCard, searchWildCard, searchWildCard, searchWildCard))
        if result:
            print(result)
        else:
            print("Customer not found.")

    def UpdateCustomer(self, customer_id, email=None, phone=None, branch_id=None):
        updates = []
        params = []

        if email:
            updates.append("email = ?")
            params.append(email)
        if phone:
            updates.append("phone = ?")
            params.append(phone)
        if branch_id:
            updates.append("branch_id = ?")
            params.append(branch_id)

        if updates:
            query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = ?"
            params.append(customer_id)
            self.db.execute_query(query, tuple(params))
            print("Customer updated successfully!")
        else:
            print("No updates were made.")
