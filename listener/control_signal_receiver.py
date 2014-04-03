import json
import socket

from settings import DATABASE_NAME
from persistent_store import PersistentStore


class ControlSignalReceiver:
    """
    This module listens for signals from the server. The server typically
    sends the client settings details like 'paths to sync', 'client ip' etc.

    It listens on port 5555.
    """
    def __call__(self, host='localhost', port='5657'):
        # Initialize the socket
        self.sock = socket.socket()
        self.sock.bind((host, int(port)))

        # Start listening
        self.sock.listen(5)

        # Always keep running
        connection, address = self.sock.accept()
        while True:
            received = connection.recv(1024)

            if received:
                self._analyze_signal(received)

    def _analyze_signal(self, signal):
        """
        The signal received will be in a JSON form. In this method, we convert
        it into a Python dict. The format of the signal is as follows:

          {
            'paths': { 'target_table': <string>,
                       'client': <string>,
                       'paths': JSON,
                  },
            'settings': { 'setting_name': <string>,
                          'value': <string>
                        },
          }

        :param signal: The signal received from the server
        :type signal: JSON string
        """
        # Signal received will be in JSON form. We've to convert to a
        # normal Python dict
        signal = json.loads(signal)

        try:
            if signal['paths']:
                storage = PersistentStore(DATABASE_NAME)
            target_table = signal['paths']['target_table']
            client = signal['paths']['client']
            paths = json.loads(signal['paths']['paths'])['paths']

            # Store the paths in the DB
            storage.set_paths(target_table, client, paths)

            print "Path database synced from server"
        except KeyError:
            print "Sync path database update from server failed"

