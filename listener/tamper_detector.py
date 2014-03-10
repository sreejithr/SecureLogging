import os

from difflib import Differ


class TamperDetector:
    """
    This will monitor periodically if the files which are being monitored are being
    tampered with. It will remember the last line till where it has already finished
    checking for tampering and check for tampering in the forecoming lines.

    If the line cannot be found at all (or portion of the line), it is automatically
    felt as tampered.
    """
    def __init__(self, list_of_files):
        self._differ = Differ()
        self._list_of_files = list_of_files

    def tamper_detect(self):
        for path in self._list_of_files:
            if _is_tampered(path, os.path.join(SNAPSHOT_PREFIX, path)):
                return True        
        return False

    def _is_tampered(self, path, older_version_path):
        current = open(path).readlines()
        snapshot = open(older_version_path).readlines()

        plus_minus = []
        for line in self._differ.compare(current, snapshot):
            plus_minus.append(line[0])

        return self._is_valid(plus_minus)

