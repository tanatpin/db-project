from jdaidb.storage_manager.page import Page
from jdaidb.storage_manager.page_directory_entry import PageDirectoryEntry
from jdaidb.storage_manager.buffer_pool import BufferPool
from jdaidb.catalog.core import Catalog
from jdaidb.common.file import write_file, read_file, create_file
import os

class StorageManager:
    def __init__(self, disk_path: str, page_size: int, buffer_size: int):
        self.disk_path = disk_path
        self.page_size = page_size

        self.catalog = Catalog(disk_path)

        self.current_page_id = 0
        self.page_directory = {}

        self.page_filepath = {}

        self.__restore()

        # TODO(A1): buffer pool initialization
        self.buffer_pool = BufferPool(buffer_size, self)


    def teardown(self):
        self.catalog.teardown()
        self.__flush()

    """
    Public Functions
    """

    # C
    def create_page(self, types) -> int:
        self.current_page_id += 1
        new_page = Page(page_size=self.page_size, types=types, tuples=[])

        # TODO(A1): put the new page into the buffer pool first
        # HINT: self.buffer_pool.put(...)
        self.buffer_pool.put(self.current_page_id, new_page)

        write_file(f"{self.disk_path}/{self.current_page_id}.page", str(new_page))
        self.page_filepath[self.current_page_id] = f"{self.disk_path}/{self.current_page_id}.page"
        self.__flush()
        
        return self.current_page_id
    
    # R
    def read_page(self, id: int) -> Page:

        page = self.buffer_pool.get(id)

        if page != None:
            return page

        path = self.__find_page(id)
        if path == None:
            raise ValueError(f"Page {id} does not exist")

        # TODO(A1): try reading the page from buffer pool
        # HINT-1: self.buffer_pool.get(...)
        # HINT-2: perhaps, you need to self.buffer_pool.put(...) to update the pool
        page_content = read_file(path)
        page = Page(page_str=page_content)

        self.buffer_pool.put(id, page)

        return page

    def get_pages_from_table(self, table_name: str) -> list[int]:
        return self.page_directory[table_name].page_ids

    def is_page_full(self, id: int) -> bool:
        return self.read_page(id).is_full()
    
    # U
    def update_page(self, id: int, updated_page: Page):
        path = self.__find_page(id)
        if path == None:
            raise ValueError(f"Page {id} does not exist")

        # TODO(A1): put the updated page into buffer pool
        # HINT: self.buffer_pool.put(...)
        self.buffer_pool.put(id, updated_page)
        write_file(path, str(updated_page))

    def add_page_to_table(self, table_name: str, page_id: int):
        if not table_name in self.page_directory:
            self.page_directory[table_name] = PageDirectoryEntry(table_name, [])
        self.page_directory[table_name].add_page(page_id)
        self.__flush()

    # U (used by buffer pool)
    def flush_page(self, id: int, updated_page: Page):
        path = self.__find_page(id)
        if path == None:
            raise ValueError(f"Page {id} does not exist")
        write_file(path, str(updated_page))

    def add_tuple_to_page(self, id: int, row: tuple) -> bool:
        page = self.read_page(id)
        page.add_tuple(row)
        self.update_page(id, page)

    # D
    def delete_page(self, id: int):
        if self.__page_exist(id):
            # TODO(A1): forcely evict the page from the buffer pool
            if self.__page_exist(id):
                self.buffer_pool.evict(id)


            os.remove(self.page_filepath[id])
            self.page_filepath.pop(id)
        else:
            raise ValueError(f"Page {id} does not exist")
        self.__flush()

    def remove_page_from_table(self, table_name: str, page_id: int):
        self.page_directory[table_name].remove_page(page_id)
        self.__flush()

    """
    Private Functions
    """

    def __page_exist(self, id: int) -> str:
        return id in self.page_filepath

    def __find_page(self, id: int) -> str:
        return self.page_filepath[id]

    def __flush(self):
        # TODO(A1): flush all in buffer pool
        # HINT: self.buffer_pool.flush_all()
        self.buffer_pool.flush_all()   

        page_filepath_str = f"{self.current_page_id}|{len(self.page_filepath.keys())}"
        for page_id in self.page_filepath.keys():
            page_filepath_str += f"|{page_id}|{self.page_filepath[page_id]}"
        page_filepath_str += "\n"
        write_file(f"{self.disk_path}/.pagepath", page_filepath_str)

        page_directory_str = ""
        for table_name in self.page_directory.keys():
            page_directory_str += str(self.page_directory[table_name])
        write_file(f"{self.disk_path}/.pagedir", page_directory_str)

    def __restore(self):
        # restore pagepath
        if not os.path.exists(f"{self.disk_path}/.pagepath"):
            return
        
        content = read_file(f"{self.disk_path}/.pagepath").strip()
        tokens = content.split("|")
        self.current_page_id = int(tokens[0])
        num_page_filepath_entry = int(tokens[1])
        for i in range(2, 2+(num_page_filepath_entry*2), 2):
            key = int(tokens[i])
            value = str(tokens[i+1])
            self.page_filepath[key] = value

        # restore pagedir
        if not os.path.exists(f"{self.disk_path}/.pagedir"):
            return
        
        content = read_file(f"{self.disk_path}/.pagedir").strip().splitlines()
        for line in content:
            line = line.strip()
            tokens = line.split("|")
            table_name = tokens[0]
            num_pages = int(tokens[1])
            page_ids = []
            for i in range(2, 2+num_pages, 1):
                page_ids.append(int(tokens[i]))
            self.page_directory[table_name] = PageDirectoryEntry(table_name, page_ids)
