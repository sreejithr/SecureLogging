"""
This module collects the log from the target machine using rsync periodically.
It also listens to a socket which would receive message in cases of:

1) Attacker tries to tamper the logs.
2) The listener python process in the target machine crashes.
3) Haven't received heartbeat signals from the target machine for long duration
"""
import socket
import sys

from .rsync import rsync_logs


class LogCollector:
    def __init__(self, target_username, target_ip):
        self.target_username = target_user
        self.target_ip = target_ip

    def _collect_logs(self):
        """
        This method collects logs from the target machine using rsync
        """
        return rsync_logs(self.target_username, self.target_ip)

if __name__ == '__main__':
    pass

