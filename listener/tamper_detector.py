import os

from difflib import Differ
from settings import SNAPSHOT_PREFIX


class TamperDetector:
    """
    This will monitor periodically if the files which are being monitored are being
    tampered with. It will remember the last line till where it has already
    finished checking for tampering and check for tampering in the forecoming
    lines.

    If the line cannot be found at all (or portion of the line), it is
    automatically declared as tampered.
    """
    def __init__(self):
        self._differ = Differ()

    def tamper_detect(self, older_version_path, path):
        current = open(path).readlines()
        snapshot = open(older_version_path).readlines()

        plus_minus = []
        for line in self._differ.compare(current, snapshot):
            plus_minus.append(line[0])

        return self._is_tampered(plus_minus, len(snapshot))

    def _is_tampered(self, plus_minus, no_of_lines_in_snapshot):
        try:
            if plus_minus.index('-') < no_of_lines_in_snapshot:
                return True
        except ValueError:
            pass
        return False

