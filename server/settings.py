import os

DATABASE_NAME = 'server_db.db'
FILES_TABLE_NAME = 'tracked_files'
CLIENTS_TABLE_NAME = 'clients'

CLIENT_NAME = 'localhost'
SERVER_HOST = 'localhost' # TODO
SNAPSHOT_PREFIX = os.path.realpath('SNAPSHOT')
CONTROL_SIGNAL_RECEIVER_PORT = 5555

CRITICAL_SETTINGS_FILE = 'critical_settings'
# For server
HEARTBEAT_INTERVAL = 5
CHECK_INTERVAL = 5

# RSync
RSYNC_BASE_DIR = os.path.realpath('LOGS')

