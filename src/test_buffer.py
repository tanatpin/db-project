from jdaidb.interface.cli import CLI
from jdaidb.query_engine.core import QueryEngine
from jdaidb.storage_manager.core import StorageManager
from jdaidb.catalog.core import Catalog
from jdaidb.parser.core import Parser

DISK_PATH = "/tmp/jdaidb"

"""
Create the 'disks' path
"""
import shutil
import os

if os.path.exists(DISK_PATH) and os.path.isdir(DISK_PATH):
    shutil.rmtree(DISK_PATH)
os.makedirs(DISK_PATH)

"""
Begin testing
"""
sm = StorageManager(disk_path=DISK_PATH, page_size=1024, buffer_size=16384)
qe = QueryEngine(storage_manager=sm)

parser = Parser(qe)

parser.process("CREATE TABLE buffer x INTEGER")
for i in range(32 * 16):
    parser.process(f"INSERT INTO buffer VALUES {i}")

parser.process("SELECT * FROM buffer")
parser.process(f"INSERT INTO buffer VALUES {999}")
parser.process("SELECT * FROM buffer")

parser.teardown()
