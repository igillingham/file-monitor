from pymongo import MongoClient

class FilesDatabase:
    """
    FilesDatabase:
    Class to abstract database CRUD operations and to manage connections
    """

    def __init__(self):
        self.client = None

    def connect(self):
        self.client = MongoClient('localhost', 27017)

    def is_connected(self):
        return self.client is not None
