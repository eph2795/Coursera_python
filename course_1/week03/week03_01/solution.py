class FileReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
            return data
        except FileNotFoundError:
            return ''