from jdaidb.query_engine.core import QueryEngine

class Parser:
    def __init__(self, engine: QueryEngine):
        self.engine = engine

    def teardown(self):
        self.engine.teardown()
    
    """
    Public Functions
    """

    def process(self, query_string: str):
        tokens = query_string.split()
        upper_tokens = query_string.upper().split()

        # CREATE TABLE [table_name] [column_name] [column_type] ...
        # jdaidb supports only INTEGER, FLOAT, VARCHAR_64
        if upper_tokens[0:2] == ["CREATE", "TABLE"] and \
            len(tokens) >= 3 and \
            len(tokens) % 2 == 1:
            table_name = tokens[2]
            column_names = []
            column_types = []
            for i in range(3, len(tokens), 2):
                column_name = tokens[i]
                column_type = upper_tokens[i+1]
                if not column_type in ("INTEGER", "FLOAT", "VARCHAR_64"):
                    raise SyntaxError(f"{column_type} is not a supported column type")
                else:
                    column_names.append(column_name)
                    column_types.append(column_type)

            self.engine.create_table(table_name, column_names, column_types)
            print(f"table {table_name} has been created")

        # DROP TABLE [table_name]
        elif upper_tokens[0:2] == ["DROP", "TABLE"] and \
            len(tokens) == 3:
            table_name = tokens[2]
            self.engine.drop_table(table_name)
            print(f"table {table_name} has been dropped")

        # INSERT INTO [table_name] VALUES [val1] [val2] ...
        elif upper_tokens[0:2] == ["INSERT", "INTO"] and upper_tokens[3] == "VALUES":
            table_name = tokens[2]
            values = tokens[4:]
            self.engine.insert_tuple_into_table(table_name, tuple(values))
            print(f"a row has been inserted into {table_name}")
        
        # SELECT * FROM [table_name]
        elif upper_tokens[0:3] == ["SELECT", "*", "FROM"] and len(tokens) == 4:
            table_name = tokens[3]
            table_string = self.engine.read_table(table_name)
            print(table_string)

        # Otherwise, treat as SyntaxError
        else:
            raise SyntaxError("syntax error.")
