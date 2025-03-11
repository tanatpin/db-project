class Customer:
    def __init__(self, db):
        self.db = db

        self.db.execute("""

            CREATE TABLE IF NOT EXISTS customer_list (
                customer_id INTEGER PRIMARY KEY,
                customer_type TEXT NOT NULL CHECK(customer_type IN ('Individual', 'Company')),
                first_name TEXT,
                last_name TEXT,
                company_name TEXT,
                email TEXT,
                phone_number TEXT,
                branch_id INTEGER,
                FOREIGN KEY (branch_id) REFERENCES customer_branches(branch_id)
                        );

        """)
    
    def NewCustomer(self, customer_type, firstName=None, lastName=None, companyName=None, email=None, phoneNum=None, branchId=None):
        if customer_type not in ['Individual', 'Company']:
            raise ValueError("Invalid customer type. Must be 'Individual' or 'Company.'")
        
        self.db.execute("""
            INSERT INTO customer_list (customer_type, first_name, last_name, company_name, email, phone_number, branch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?) 
        """, (customer_type, firstName, lastName, companyName, email, phoneNum, branchId))

        print("New customer added successfully!")


    def SearchCustomer(self, customerId):
        result = self.db.execute("SELECT * FROM customer_list WHERE customer_id = ?", (customerId,)).fetchone()

        if result:
            print(f"Customer ID: {result[0]}, Type: {result[1]}, Name: {result[2]} {result[3] if result[1] == 'Individual' else result[4]}")
        else:
            print("Customer not found.")


    
    def UpdateCustomer(self, customer_id, firstName=None, lastName=None, companyName=None, email=None, phoneNum=None, branchId=None):
        existing_customer = self.db.execute("SELECT * FROM customer_list WHERE customer_id = ?", (customer_id,)).fetchone()

        if not existing_customer:
            print("Customer not found.")
            return

        updates = []
        values = []

        if firstName:
            updates.append("first_name = ?")
            values.append(firstName)

        if lastName:
            updates.append("last_name = ?")
            values.append(lastName)

        if companyName:
            updates.append("company_name = ?")
            values.append(companyName)

        if email:
            updates.append("email = ?")
            values.append(email)

        if phoneNum:
            updates.append("phone_number = ?")
            values.append(phoneNum)

        if branchId:
            updates.append("branch_id = ?")
            values.append(branchId)

        values.append(customer_id)

        self.db.execute(f"""
            UPDATE customer_list
            SET {', '.join(updates)}
            WHERE customer_id = ?
        """, values)

        print("Customer updated successfully!")

