class CustomerBranch:
    def __init__(self, db):
        self.db = db
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS customer_branches (
                branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                branch_name TEXT,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL
            );
        """)


    def AddBranch(self, branch_name, address, city, country):
        self.db.execute("""
            INSERT INTO customer_branches (branch_name, address, city, country)
            VALUES (?, ?, ?, ?)
        """, (branch_name, address, city, country))
        print("Branch/Address added successfully!")


    def SearchBranch(self, branch_id):
        branch = self.db.execute("""
            SELECT branch_name, address, city, country FROM customer_branches WHERE branch_id = ?
        """, (branch_id,)).fetchone()

        if branch:
            print(f"Branch ID: {branch_id}")
            print(f"Branch Name: {branch[0] if branch[0] else 'N/A'}")
            print(f"Address: {branch[1]}, {branch[2]}, {branch[3]}")
        else:
            print("Branch/Address not found.")
