from jdaidb.storage_manager.page import Page
# from jdaidb.storage_manager.storage_manager import StorageManager # remove since cyclic import

class BufferPool:
    def __init__(self, num_slots: int, storage_manager):
        self.storage_manager = storage_manager

        self.num_slots = num_slots
        self.num_pages = 0

        # list of pages (i.e., page IDs)
        self.page_ids = [-1] * self.num_slots
        self.pages = [None] * self.num_slots

        # TODO(A1): add more local variables (if needed)
        self.lruList = []


    """
    Public Functions
    """
    
    # TODO(A1): read the page in the database 
    def get(self, id: int) -> Page:
        if id in self.page_ids:
            self.lruList.remove(id)
            self.lruList.append(id)

            idx = self.page_ids.index(id)

            getPage = self.pages[idx]

            return getPage

        # If id isn't found in the page ids list, then just return None 
        return None


    # TODO(A1): write the page in the database 
    def put(self, id: int, updated_page: Page):

        if id in self.page_ids:
            idx = self.page_ids.index(id) 
            self.pages[idx] = updated_page

            self.lruList.remove(id)
            self.lruList.append(id)
       
        else:
            if self.num_slots > self.num_pages:
                idx = self.page_ids.index(-1)

                self.page_ids[idx] = id
                self.pages[idx] = updated_page
                self.num_pages += 1
            
            else:
                idx = self.evict()

                self.page_ids[idx] = id
                self.pages[idx] = updated_page
            
            self.lruList.append(id)

        return id

    # use by storage manager
    def flush_all(self):
        for i in range(self.num_slots):
            if self.page_ids[i] != -1:
                self.storage_manager.flush_page(self.page_ids[i], self.pages[i])

    # TODO(A1): evict the page based on the LRU policy
    #           if id is None, just evict without replacing
    #           if id is not None, evict and replace with the page with id
    def evict(self, id=None) -> int:
        
        if id == None:
            id = self.lruList[0]
    
        idx = self.page_ids.index(id)
        self.page_ids[idx] = -1
        self.pages[idx] = None
        self.lruList.pop(self.lruList.index(id)) 

        return idx

    """
    Private Functions
    """

    # TODO:
    def pin_page(self, id: int, new_page: Page) -> int:

        #The purpose of this function is to bring a specific page into the buffer pool and ensure that it is pinned which means it cant be evicted

        if id in self.page_ids:
            idx = self.page_ids.index(id)
            self.pages[idx] = new_page
            self.lruList.remove(id)
            self.lruList.append(id)
        
        # If this id does not exist in the buffer pool, add it
        else:
            self.put(id, new_page)
            idx = self.page_ids.index(id)

        return idx
