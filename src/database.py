import duckdb

class Database:
    def __init__(self, dbName = "companyDB.db"):
        self.conn = duckdb.connect(dbName)
        
    def execute(self, query, param = ()):
        return self.conn.execute(query, param)