"""
This script should listen to the changes to a particular file and inspect for
any tampering. After a fixed amount of changes/time, it should send the diff to
the remote server.

If tampering has been detected, it should alert the remote server first and send
the diff/file as a whole.
"""
import os
import sys
import time
import socket
import threading
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tamper_detector import TamperDetector
from persistent_store import PersistentStore
from settings import (SNAPSHOT_PREFIX, DATABASE_NAME, FILES_TABLE_NAME, CLIENT_NAME)

PATH = "/Users/sreejith/pics"
TARGET = "digitalocean:/home/sreejith/pics"

CHANGE_COUNT = 0
NO_OF_CHANGES_FOR_SNAPSHOTTING = 1


def make_snapshots():
    """
    Makes copy of the files for doing diffs on
    """
    list_of_paths = PersistentStore(DATABASE_NAME).get_paths(FILES_TABLE_NAME,
                                                             CLIENT_NAME)
    for path in list_of_paths:
        path_backslash_removed = path[1:] if path[0] == '/' else path
        if os.path.isdir(path):
            target_path = os.path.join(SNAPSHOT_PREFIX,
                                       os.path.split(path_backslash_removed)[0])
        else:
            target_path = os.path.join(SNAPSHOT_PREFIX, path_backslash_removed)

        if not os.path.exists(target_path):
            subprocess.call(['mkdir','-p', target_path])

        subprocess.call(['cp', '-r', path, target_path])


class FileChangeEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        tamper_detector = TamperDetector()
        path = event.src_path
        print "Change detected"

        self.all_files = []
        if os.path.isdir(path):
            self.get_filenames(path, save_to=self.all_files)

        try:
            target_path = os.path.join(SNAPSHOT_PREFIX, path[1:]
                                       if path[0] == '/' else path)
            if self.all_files:
                for file_name in self.all_files:
                    if tamper_detector.tamper_detect(target_path, file_name):
                        print "Tampered"
                    else:
                        make_snapshots()
            else:
                if tamper_detector.tamper_detect(target_path, path):
                    print "Tampered"
                else:
                    make_snapshots()
        except IOError:
            pass

    def get_filenames(self, path, save_to):
        for each, _, files in os.walk(path):
            for file_name in files:
                self.all_files.append(os.path.join(each, file_name))


class FileTracker:
    """
    It will monitor changes to the file.
    """
    def __init__(self, list_of_files):
        self._list_of_files = list_of_files

    def start_observing(self):
        observer = Observer()
        filechange_event_handler = FileChangeEventHandler()

        make_snapshots()
        for path in self._list_of_files:
            observer.schedule(filechange_event_handler, path, recursive=True)
        observer.start()
        while True:
            time.sleep(1)
        observer.stop()
        observer.join()

    def _alert_server(self):
        # TODO
        pass


if __name__ == '__main__':
    while True:
        time.sleep(1)
#    path = sys.argv[1] if len(sys.argv[1] > 1) else '.'
#    file_change_handler = FileChangeHandler()

