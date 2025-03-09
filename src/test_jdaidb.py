import sys

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

catalog = Catalog(disk_path=DISK_PATH)
sm = StorageManager(disk_path=DISK_PATH, page_size=1024, buffer_size=16384)
qe = QueryEngine(catalog=catalog, storage_manager=sm)
parser = Parser(qe)

def test_simple():
    parser.process("CREATE TABLE abc id INTEGER name VARCHAR_64 salary FLOAT")
    parser.process("SELECT * FROM abc")
    parser.process("INSERT INTO abc VALUES 1 Alice 50.5")
    parser.process("INSERT INTO abc VALUES 2 Bob 21.4")
    parser.process("INSERT INTO abc VALUES 3 Charles 10.3")
    parser.process("SELECT * FROM abc")
    parser.process("DROP TABLE abc")
    parser.teardown()

    return True

def test_buffer():
    parser.process("CREATE TABLE buffer x INTEGER")
    for i in range(32 * 16):
        parser.process(f"INSERT INTO buffer VALUES {i}")
    parser.process("DROP TABLE buffer")
    parser.teardown()

    return True

def test_error1():
    is_passed = True

    try:
        parser.process("CREATE TABLE abc id INTEGER name VARCHAR_64 salary FLOAT")
        parser.process("INSERT INTO abc VALUES 2 21.4 Bob")
        is_passed = False
    except ValueError:
        pass

    parser.process("DROP TABLE abc")
    parser.teardown()

    return is_passed

def test_error2():
    is_passed = True

    try:
        parser.process("CREATE TALE abc id INTEGER name VARCHAR_64 salary FLOAT")
        is_passed = False
    except SyntaxError:
        pass

    parser.teardown()

    return is_passed

def test_error3():
    is_passed = True

    try:
        parser.process("CREATE TABLE abc id INTEGER name VARCHAR_64 salary FLOAT")
        parser.process("CREATE TABLE abc id INTEGER name VARCHAR_64 salary FLOAT")
        is_passed = False
    except ValueError:
        pass

    parser.process("DROP TABLE abc")
    parser.teardown()

    return is_passed

tests = [test_simple, test_buffer, test_error1, test_error2, test_error3]
for test in tests:
    original_stdout = sys.stdout
    sys.stdout = None
    test_result = test()
    sys.stdout = original_stdout

    if test_result:
        print(f"test {test} OK")
    else:
        print(f"test {test} Not OK")
        sys.exit()
