""" dbmanager:
Author: Ian Gillingham
Date: 7 March 2019

This module abstracts the MongoDb database interface.
The filedata json data is structured thus:
{"filename":"",
 "filepath":"",
 "filesize":"",
 "creationtume":"",
 "modifiedtime":""
 "archived": ""}
"""
import time, threading
from pymongo import MongoClient



class FilesDatabase:
    """
    FilesDatabase:
    Class to abstract database CRUD operations and to manage connections
    """
    __dbname = "filemon"
    __colname = "filedata"

    # Define the shelf-life of files in seconds. Nominal is 5 days (432000 s)
    __seconds_to_archive = 600

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        # self.watch_file_times(self)  # Start the file time scanner

    def watch_file_times(self, this):
        """
        Self repeating timer callback, to test all database entries for modified times in excess
        of the archive cutoff.
        :return: Nothing
        """
        print("File time to archive scan")
        this.scan_for_archive_time(this)
        threading.Timer(5, this.watch_file_times).start()

    def connect(self):
        """ connect():
        Connect to the MongoDb service.
        Reference the filemon database.
        reference the filedata collection
        :return: bool
        """
        ret = False  # Guilty until proven otherwise
        self.client = MongoClient('localhost', 27017)

        # Send a query to the server to see if the connection is working.
        try:
            self.client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Unable to find MongoDb server")
            self.client = None

        if self.client is not None:
            self.db = self.client[self.__dbname]
            self.collection = self.db[self.__colname]
            ret = True
        return ret

    def is_connected(self):
        return self.client is not None

    def create_entry(self, file_data):
        """ create_entry():
        Creates a new entry in the database for a file that has been detected in the monitored directory.
        :param file_data:
        :return:
        """
        self.collection.insert_one(file_data)

    def update_entry(self, file_data):
        """ update_entry():
        Searches for the filename in the database and if found, updates the modified time
        :param file_data:
        :return:
        """
        print("update: file_data -> ", file_data)
        self.collection.find_one_and_replace({"name": file_data['name']}, file_data, upsert=True)

    def delete_entry(self, file_data):
        """ delete_entry():
        Searches for the filename in the database and if found, deletes the document
        :param file_data:
        :return:
        """
        self.collection.find_one_and_delete({"name": file_data['name']})

    def get_all_entries(self):
        """ get_all_entries():
        Return a list of all available file entries in database
        :param None:
        :return: array of dictionaries
        """
        filelist = []
        for doc in self.collection.find({}):
            item = {'name': doc['name'],
                    'path': doc['path'],
                    'created': doc['created'],
                    'modified': doc['modified']}
            print(item)
            filelist.append(item)

        ret = filelist

        print("All find(): ", ret)
        return ret

    def get_available_entries(self):
        """ get_available_entries():
        Return a list of available file entries in database
        :param None:
        :return: array of dictionaries
        """
        filelist = []
        for doc in self.collection.find({}):
            if doc['archived'] == "":
                item = {'name': doc['name'],
                        'path': doc['path'],
                        'created': doc['created'],
                        'modified': doc['modified']}
                print(item)
                filelist.append(item)

        ret = filelist

        print("Available find(): ", ret)
        return ret

    def get_archived_entries(self):
        """ get_archived_entries():
        Return a list of archived file entries in database
        :param None:
        :return: array of dictionaries
        """
        filelist = []
        for doc in self.collection.find({}):
            if doc['archived'] != "":
                item = {'name': doc['name'],
                        'path': doc['path'],
                        'created': doc['created'],
                        'modified': doc['modified']}
                print(item)
                filelist.append(item)

        ret = filelist

        print("Archived find(): ", ret)
        return ret

    def scan_for_archive_time(self, this):
        """
        Iterate ove the collection and tag any entries which have a modified time in excess of the archive time
        as archived.
        :return: Nothing
        """
        current_time = time.time()

        # Calculate the cutoff time, before which a file should be tagged as archived
        archive_time = current_time - this.__seconds_to_archive
        #this.collection.update_many({"created": "$gt:"+str(archive_time)}, {"archived": "1"})


# Create a singleton instance of the database manager
db = FilesDatabase()



