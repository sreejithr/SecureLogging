import threading

from heartbeat_server import HeartbeatServer
from .settings import (SERVER_HOST, SERVER_PORT, HEARTBEAT_INTERVAL,
                       CHECK_INTERVAL, LOG_COLLECT_INTERVAL, DATABASE_NAME,
                       CLIENTS_TABLE_NAME, FILES_TABLE_NAME)

def start_log_collection():
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


if __name__ == '__main__':
    heartbeat_server = HeartbeatServer(SERVER_HOST, SERVER_PORT, HEARTBEAT_INTERVAL,
                                       CHECK_INTERVAL)

    heartbeat_server_thread = threading.Thread(target=heartbeat_server.serve)
    heartbeat_server_thread.daemon = True
    heartbeat_server_thread.run()

    log_collector_thread = threading.Thread(target=start_log_collection)
    log_collector_thread.daemon = True
    log_collector_thread.run()

