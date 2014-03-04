"""
This script should listen to the changes to a particular file and inspect for
any tampering. After a fixed amount of changes/time, it should send the diff to
the remote server.

If tampering has been detected, it should alert the remote server first and send
the diff/file as a whole.
"""
import sys
import time
import socket
import threading

from watchdog.observers import Observer
from difflib import ndiff

PATH = "/Users/sreejith/pics"
TARGET = "digitalocean:/home/sreejith/pics"


class FileChangeHandler:
    """
    It will monitor changes to the file.
    """
    def __call__(self):
        """
        On call, it should perform tamper-detection, and pass it onto the
        CommunicationHandler
        """
        pass


class HeartbeatSender:

    def __init__(self, target_host, target_port):
        self._target_host = target_host
        self._target_port = target_port

    def start_heartbeat_sending(self, time_period=300):
        """
        It starts a timer for the given 'time_period' (in seconds) and executes
        the _log_send() function every time period (say, 300s = 5min).

        :param time_period: _log_send() is executed every 'time_period' seconds
        :type time_period: int
        """
        # We're just making sure time_period is an int by explicitly converting
        # it to int. If it is something like 'abc' which is not an int, a
        # ValueError will occur. In that case, we set the time to 300sec manually.
        try:
            time_period = int(time_period)
        except ValueError:
            time_period = 300

        timer_task = threading.Timer(time_period, self._send_heartbeat, [time_period])
        # When the main program (main process) exits, we also want this thread
        # to exit. Otherwise, it will still keep sending heartbeats to the server
        # which gives a false impression to the server that the listener process
        # is still alive.
        timer_task.daemon = True
        # Start timer
        timer_task.start()

    def _send_heartbeat(self, time_period):
        """
        Sends a simple "beat" string to the specified target
        """
        self.sock = socket.socket()
        self.sock.connect((self._target_host, int(self._target_port)))        
        while True:
            self.sock.send("beat")
            print "hey"
            time.sleep(time_period)
        self.sock.close()


class DiffExtractor:
    """
    This will make a diff of the file when a change is detected.
    """
    def _extract_diff(self):
        """
        Extracts diff
        """
        pass

if __name__ == '__main__':
    heartbeat_sender = HeartbeatSender('localhost', 5656)
    heartbeat_sender.start_heartbeat_sending(5)

    while True:
        time.sleep(1)
#    path = sys.argv[1] if len(sys.argv[1] > 1) else '.'
#    file_change_handler = FileChangeHandler()

#    observer = Observer()
#    observer.schedule(event_handler, path, recursive=True)
#    observer.start()

#    try:
#        time.sleep(1)
#    except KeyboardInterrupt:
#        observer.stop()
#    observer.join()

