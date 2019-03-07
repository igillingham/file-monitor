""" file_manager:
Author: Ian Gillingham
Date: 7 March 2019

This module handles all filesystem events, detecting changes to the specified path
and updating the database accordingly, vi the dbmanager module.

Note: Under Linux, a file original creation date is not stored, so we can infer it from
      the time it was first seen and inserted in the database.
"""

import sys
import time
import os.path
import json
import dbmanager
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


__observer = Observer()

ERR_NO_ERROR = 0
ERR_NO_DIR = 1000
ERR_NO_CONF = 1001


class FileMetadata:
    def __init__(self, path):
        self.path = path
        self.dir, self.name = os.path.split(path)
        if os.path.isfile(path):
            self.created = os.stat(path).st_ctime
            self.modified = self.created
        else:
            self.created = 0
            self.modified = 0

    def json(self):
        obj_json = {"path": self.path,
                    "name": self.name,
                    "created": self.created,
                    "modified": self.modified}
        return obj_json


class RHEAChangeHandler(PatternMatchingEventHandler):
    patterns = ["*.*"]

    def on_modified(self, event):
        metadata = FileMetadata(event.src_path)
        dbmanager.db.update_entry(metadata.json())

    def on_deleted(self, event):
        metadata = FileMetadata(event.src_path)
        dbmanager.db.delete_entry(metadata.json())

    def on_created(self, event):
        metadata = FileMetadata(event.src_path)
        dbmanager.db.create_entry(metadata.json())


def rhea_monitor_fs():
    """ rhea_monitor_fs():
        Start the filesystem watchdog, specifically monitoring the
        directory defined in the project conf.json file.
    """
    ret = ERR_NO_CONF  # Assume conf does not exist until we open it
    dirname = None
    with open('conf.json') as json_file:
        conf = json.load(json_file)
        if 'filesdir' in conf.keys():
            dirname = conf['filesdir']

    if dirname is not None:
        if os.path.isdir(dirname):
            __observer.schedule(RHEAChangeHandler(), dirname)
            __observer.start()
            ret = ERR_NO_ERROR
        else:
            ret = ERR_NO_DIR

    return ret


"""
__main__: Stub code to execute if this module is run directly from the command line.
"""
if __name__ == '__main__':
    args = sys.argv[1:]
    __observer.schedule(RHEAChangeHandler(), path=args[0] if args else '.')
    __observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        __observer.stop()

    __observer.join()
