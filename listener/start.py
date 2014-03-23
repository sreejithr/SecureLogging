import sys
import time
import threading

from persistent_store import PersistentStore
from control_signal_receiver import ControlSignalReceiver
from heart_beat import HeartbeatSender
from listener import FileTracker
from settings import (SERVER_HOST, SERVER_PORT, DATABASE_NAME, FILES_TABLE_NAME,
                      CLIENT_NAME, HEARTBEAT_TIMING)

if __name__ == '__main__':
    tamper_detection = True if 'tamper_detect' in sys.argv else False
    paths = PersistentStore(DATABASE_NAME).get_paths(FILES_TABLE_NAME, CLIENT_NAME)

    heartbeat_sender = HeartbeatSender(SERVER_HOST, SERVER_PORT)
    heartbeat_thread = threading.Thread(target=heartbeat_sender\
                                        .start_heartbeat_sending,
                                        args=(HEARTBEAT_TIMING,))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    control_signal_receiver = ControlSignalReceiver()
    control_signal_thread = threading.Thread(target=control_signal_receiver)
    control_signal_thread.daemon = True
    control_signal_thread.start()

    if tamper_detection:
        file_tracker = FileTracker(paths)
        filetracker_thread = threading.Thread(
            target=file_tracker.start_observing)
        filetracker_thread.daemon = True
        filetracker_thread.start()

    while True:
        time.sleep(1)
            
