class PageDirectoryEntry:
    def __init__(self, table_name: str, page_ids=[]):
        self.table_name = table_name
        self.page_ids = page_ids

    def __str__(self):
        text = f"{self.table_name}|{len(self.page_ids)}"
        for page_id in self.page_ids:
            text += f"|{page_id}"
        return text + "\n"

    """
    Public Functions
    """

    # C
    def add_page(self, page_id: int):
        if page_id in self.page_ids:
            raise ValueError(f"page {page_id} has already been added.")
        self.page_ids.append(page_id)
    
    # D
    def remove_page(self, page_id: int):
        if not page_id in self.page_ids:
            raise ValueError(f"page {page_id} has not already been added.")
        self.page_ids.remove(page_id)
