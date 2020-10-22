import os
import tempfile
import uuid


class File():
    def __init__(self, path):
        """
        passed full path to file
        if file not exist, create a new one
        """
        self.position = 0
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'w'):
                pass

    def write(self, string):
        """write content to file"""
        with open(self.path, 'w') as f:
            return f.write(string)

    def read(self):
        """return file content"""
        with open(self.path, 'r') as f:
            return f.read()

    def __add__(self, second_file):
        """
        Create a new instance of File, and new file in temdir
        Also write content of both files to new file
        The file name will be unique
        """
        new_file_path = os.path.join(
            tempfile.gettempdir(),
            str(uuid.uuid4().hex)
            )
        with open(new_file_path, 'w') as f:
            f.write(File.read(self) + File.read(second_file))
        return File(new_file_path)

    def __str__(self):
        """return full path to file"""
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        self.content = open(self.path, 'r').readlines()
        if self.positiom >= len(self.content):
            self.position = 0
            raise StopIteration
        result = self.content[self.position]
        self.cursor += 1
        return result
