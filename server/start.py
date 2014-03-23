import json
import time
import threading
import sqlite3

from heartbeat_server import HeartbeatServer
from log_collector import LogCollector
from user_settings import (SERVER_PORT, LOG_COLLECT_INTERVAL, HEARTBEAT_TIMING)
from settings import (SERVER_HOST, HEARTBEAT_INTERVAL, CHECK_INTERVAL,
                      DATABASE_NAME, CLIENTS_TABLE_NAME, FILES_TABLE_NAME)

def start_log_collection():
    db = sqlite3.connect(DATABASE_NAME)
    db_cursor = db.cursor()
    while True:
        for client, username in db_cursor.execute(
                'select ip, username from {};'.format(CLIENTS_TABLE_NAME)):
            for paths_as_json in db_cursor.execute('select paths from {} '\
                                                   'where ip="{}";'.format(
                                                            FILES_TABLE_NAME,
                                                            client)):
                paths = json.loads(paths_as_json[0])['paths']
                log_collector = LogCollector(username, client, paths)
                log_collector.collect()
        time.sleep(LOG_COLLECT_INTERVAL)


if __name__ == '__main__':
    try:
        heartbeat_server = HeartbeatServer('localhost', int(SERVER_PORT),
                                           HEARTBEAT_INTERVAL, CHECK_INTERVAL)
    except ValueError:
        print "Check if settings are valid"

    with open('heartbeat_record.record', 'w') as f:
        f.write('{}- OK'.format(time.clock()))

    heartbeat_server_thread = threading.Thread(target=heartbeat_server.serve)
    heartbeat_server_thread.daemon = True
    heartbeat_server_thread.start()

    log_collector_thread = threading.Thread(target=start_log_collection)
    log_collector_thread.daemon = True
    log_collector_thread.start()

    while True:
        time.sleep(1)

