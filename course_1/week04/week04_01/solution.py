import os
from tempfile import gettempdir


class File:

    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                pass
        self._iter = None

    def read(self):
        with open(self.file_name, 'r') as f:
            return f.read()

    def write(self, content):
        with open(self.file_name, 'w') as f:
            f.write(content)

    def __iter__(self):
        self._iter = open(self.file_name, 'r')
        return self

    def __next__(self):
        try:
            return next(self._iter)
        except StopIteration:
            self._iter.close()
            raise StopIteration

    def __str__(self):
        return os.path.abspath(self.file_name)

    def __add__(self, other):
        _, file_name = os.path.split(self.file_name)
        new_file_path = os.path.join(gettempdir(), file_name)
        new_file = File(new_file_path)
        new_file.write(self.read() + other.read())
        return new_file
