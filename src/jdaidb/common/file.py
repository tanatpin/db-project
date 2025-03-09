def read_file(filepath: str) -> bytes:
    f = open(filepath, "r")
    data = f.read()
    f.close()
    return data

def write_file(filepath: str, content: str):
    f = open(filepath, "w")
    f.write(content)
    f.close()

def create_file(filepath: str):
    f = open(filepath, "x")
    f.close
