import os

DATABASE_NAME = 'server_db.db'
FILES_TABLE_NAME = 'tracked_files'
CLIENTS_TABLE_NAME = 'clients'

CLIENT_NAME = 'localhost'
SERVER_HOST = 'localhost' # TODO
SNAPSHOT_PREFIX = os.path.realpath('SNAPSHOT')
CONTROL_SIGNAL_RECEIVER_PORT = 5657

CRITICAL_SETTINGS_FILE = 'user_settings'
# For server
CHECK_INTERVAL = 5
BACKUP_PATH = os.path.realpath(CLIENT_NAME)

# RSync
RSYNC_BASE_DIR = os.path.realpath('LOGS')

