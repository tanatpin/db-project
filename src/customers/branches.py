class CustomerBranch:
    def __init__(self, db):
        self.db = db

    def AddBranch(self, branch_name, address, city, country):
        query = """
        INSERT INTO branches (branch_name, address, city, country)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (branch_name, address, city, country))
        print("Branch added successfully!")

    def SearchBranch(self, branch_id):
        query = "SELECT * FROM branches WHERE branch_id = ?"
        result = self.db.fetch_query(query, (branch_id,))
        if result:
            print(result)
        else:
            print("Branch not found.")
