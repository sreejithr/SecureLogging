"""
This module collects the log from the target machine using rsync periodically.
It also listens to a socket which would receive message in cases of:

1) Attacker tries to tamper the logs.
2) The listener python process in the target machine crashes.
3) Haven't received heartbeat signals from the target machine for long duration
"""
import time
import json
import sys
import sqlite3

from rsync import rsync_logs
from user_settings import LOG_COLLECT_INTERVAL
from settings import (DATABASE_NAME, FILES_TABLE_NAME, CLIENTS_TABLE_NAME)


class LogCollector:
    def __init__(self, target_username, target_ip, target_paths):
        self._target_username = target_username
        self._target_ip = target_ip
        self._target_paths = target_paths

    def collect(self):
        failed_paths = []
        for path in self._target_paths:
            try:
                if not rsync_logs(self._target_username, self._target_ip,
                                  self._target_paths):
                    failed_paths.append(path)
            except:
                failed_paths.append(path)
                print "Path '{}' could be invalid".format(path)

        if failed_paths:
            print "RSync failed for files:"
            for num, path in enumerate(failed_paths):
                print "{}. {}".format(num, path)
        else:
            print "Rsync successful"

        # Print the time for future reference
        print time.clock()
        
    
if __name__ == '__main__':
    self._db = sqlite3.connect(DATABASE_NAME)
    self._db_cursor = self._db.cursor()

    while True:
        for client, username in self._db_cursor.execute('select ip, username from {};'
                                                        .format(CLIENTS_TABLE_NAME)):
            for paths_as_json in self._db_cursor.execute('select paths from {} '\
                                                        'where client={};'.format(
                                                            FILES_TABLE_NAME, client)):
                paths = json.loads(paths_as_json)['paths']
                log_collector = LogCollector(username, client, paths)
                log_collector.collect()
        time.sleep(LOG_COLLECT_INTERVAL)

