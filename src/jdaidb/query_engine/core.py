from jdaidb.catalog.core import Catalog
from jdaidb.storage_manager.core import StorageManager

class QueryEngine():
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager
        self.catalog = self.storage_manager.catalog

    def teardown(self):
        self.storage_manager.teardown()

    """
    Public Functions
    """

    # CREATE TABLE
    def create_table(self, table_name: str, column_names: list[str], column_types: list[str]):
        self.catalog.add_table_entry(table_name, column_names, column_types)
        page_id = self.storage_manager.create_page(column_types)
        self.storage_manager.add_page_to_table(table_name, page_id)
    
    # DROP TABLE
    def drop_table(self, table_name: str):
        page_ids = self.catalog.get_pages_from_table(table_name)
        for page_id in page_ids:
            self.storage_manager.remove_page_from_table(table_name, page_id)
            self.storage_manager.delete_page(page_id)
        self.catalog.remove_table_entry(table_name)

    # INSERT
    def insert_tuple_into_table(self, table_name: str, row: tuple[...]):
        # check type
        types = self.catalog.get_types_from_table(table_name)
        for i in range(len(types)):
            if types[i] == "INTEGER":
                int(row[i])
            elif types[i] == "FLOAT":
                float(row[i])
            elif types[i] == "VARCHAR_64":
                str(row[i])
            else:
                raise ValueError(f"type {types[i]} does not exist")

        page_ids = self.storage_manager.get_pages_from_table(table_name)

        is_inserted = False
        for page_id in page_ids:
            # if can insert tuple
            if not self.storage_manager.is_page_full(page_id):
                is_inserted = True
                self.storage_manager.add_tuple_to_page(page_id, row)
        
        # if all pages are full, create a new page
        if not is_inserted:
            types = self.catalog.get_types_from_table(table_name)
            page_id = self.storage_manager.create_page(types)
            self.storage_manager.add_page_to_table(table_name, page_id)
            self.storage_manager.add_tuple_to_page(page_id, row)
        
    # SELECT *
    def read_table(self, table_name: str) -> str:
        COLUMN_SIZE = 13

        text = ""
        header, num_col = self.catalog.get_table_header(table_name)
        text += header
        row_count = 0
        page_ids = self.storage_manager.get_pages_from_table(table_name)
        for page_id in page_ids:
            page = self.storage_manager.read_page(page_id)
            for row in page.get_all_tuples():
                if row_count == 0:
                    text += "├" + ((("─" * COLUMN_SIZE) + "┼") * (num_col - 1)) + ("─" * COLUMN_SIZE) + "┤" + "\n"

                if row_count < 10:
                    text += "│"
                    for value in row:
                        text += str(value).center(COLUMN_SIZE, " ")
                        text += "│"
                    text += "\n"

                row_count += 1

        if row_count > 10:
            text += "│"
            for value in ["..."] * num_col:
                text += str(value).center(COLUMN_SIZE, " ")
                text += "│"
            text += "\n"

        text += "└" + ((("─" * COLUMN_SIZE) + "┴") * (num_col - 1)) + ("─" * COLUMN_SIZE) + "┘" + "\n"
        
        text += f"(Result: {row_count} row(s))"

        return text
