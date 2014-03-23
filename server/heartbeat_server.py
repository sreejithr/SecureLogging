import time
import socket
import threading


class HeartbeatServer:
    def __init__(self, host, port, heartbeat_interval, check_interval=50):
        self._last_heartbeat_time = None

        self._heartbeat_interval = heartbeat_interval

        self._host = host
        self._port = port
        try:
            self._check_interval = int(check_interval)
        except ValueError:
            print "Invalid check_interval value given. Defaulting to 50sec"
            self._check_interval = 50

        # Start the socket
        self._sock = socket.socket()
        self._sock.bind((self._host, self._port))
        
    def serve(self):
        # Start listening
        self._sock.listen(5)

        # Check if we are receiving heartbeats regularly. Do this
        # every `check_interval` seconds
        heartbeat_check_timer = threading.Timer(self._check_interval,
                                                self._check_heartbeats)
        heartbeat_check_timer.daemon = True
        heartbeat_check_timer.start()
        
        # Keep on running always
        connection, address = self._sock.accept()
        while True:
            received = connection.recv(1024)
            if received:
                self._last_heartbeat_time = time.clock()
                print "Got heartbeat from {}".format(address)
            else:
                pass

    def _check_heartbeats(self):
        """
        Checks if the difference in time between last heartbeat and now is
        within an acceptable range.
        """
        # We can tolerate a little error. 20% excess time is forgiveable.
        tolerance = 0.20 * self._check_interval

        # Make sure self._last_heartbeat_time and self._second_last_heartbeat_time
        # aren't `None`.
        while True:
            if self._last_heartbeat_time:
                if (time.clock() - self._last_heartbeat_time) > \
                  self._check_interval + tolerance:
                    print "Client dead"
                    with open('heartbeat_record.record', 'a') as f:
                        f.write('{} - CLIENT DEAD'.format(time.clock()))
            time.sleep(self._check_interval)

if __name__ == '__main__':
    heartbeat_server = HeartbeatServer('localhost', 5656, heartbeat_interval=5,
                                       check_interval=5)
    heartbeat_server.serve()
    
