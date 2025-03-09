class Page:
    def __init__(self, page_size=1024, types=[], tuples=[], page_str=None):
        if not page_str is None:
            lines = page_str.strip().splitlines()
            self.page_size = int(lines[0])
            self.types = lines[1].strip().split(",")
            self.tuples = []

            # tuples
            for line in lines[2:]:
                tokens = line.split(",")
                row = []
                for i in range(len(tokens)):
                    if self.types[i] == "INTEGER":
                        row.append(int(tokens[i]))
                    elif self.types[i] == "FLOAT":
                        row.append(float(tokens[i]))
                    elif self.types[i] == "VARCHAR_64":
                        row.append(str(tokens[i]))
                    else:
                        raise ValueError(f"type {self.types[i]} mismatched")
                self.tuples.append(tuple(row))
        else:
            self.types = types
            self.tuples = tuples
            self.page_size = page_size

        # let's make an assumption that all the types use 32 bytes
        self.tuple_size = 32 * len(self.types)
        # compute the max number of tuples
        self.max_tuples = self.page_size // self.tuple_size

    def __str__(self) -> str:
        text = f"{self.page_size}\n"

        # add types
        for i in range(len(self.types)):
            text += f"{self.types[i]}"
            if i < len(self.types) - 1:
                text += ","
        text += "\n"

        # add tuples
        for row in self.tuples:
            row_text = ""
            for i in range(len(row)):
                row_text += f"{row[i]}"
                if i < len(row) - 1:
                    row_text += ","
            text += row_text + "\n"
        return text

    """
    Public Functions
    """

    # C
    def add_tuple(self, new_tuple: tuple[...]):
        self.tuples.append(new_tuple)

    # R
    def get_all_tuples(self):
        return self.tuples

    # D
    def remove_tuple(self, index: int):
        self.tuples.pop(index)

    def length(self) -> int:
        return len(self.tuples)

    def is_full(self) -> bool:
        return len(self.tuples) >= self.max_tuples
