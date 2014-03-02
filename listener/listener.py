"""
This script should listen to the changes to a particular file and inspect for
any tampering. After a fixed amount of changes/time, it should send the diff to
the remote server.

If tampering has been detected, it should alert the remote server first and send
the diff/file as a whole.
"""
import sys
import subprocess

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


class LogFileSender:

    def _log_send(self):
        """
        This function sends the contents of the PATH specified to the TARGET path
        via rsync.

        RSync is a program which synchronized directories in 2 different places.
        When invoked, it compares the 2 paths and only sends files which are
        necessary for them to stay synchronized. It doesn't send all of the files.
        It sends files over SSH (Secure Shell).
        """
        # This is how you call a command line code inside python. The below line
        # calls:
        #     rsync -rave "ssh -l <TARGET-USERNAME>" --delete <SOURCE> <TARGET>
        #
        subprocess.call(["rsync", "-rave", "ssh -l sreejith", "--delete", PATH, TARGET])
        print "Synced successful"

    def start_periodic_log_sending(self, time_period=300)
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
            time = int(time_period)
        except ValueError:
            time = 300

        timer_task = threading.Timer(time, self._log_send)
        # Start timer
        timer_task.start()


class DiffExtractor:
    """
    This will make a diff of the file when a change is detected.
    """
    def _extract_diff(self):
        """
        Extracts diff
        """
        pass


class CommunicationHandler:
    """
    This would coordinate the whole process and send the diff to the remote
    server using a socket connection.
    """
    pass

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv[1] > 1) else '.'
    file_change_handler = FileChangeHandler()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

