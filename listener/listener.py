import sys
import time

from watchdog.observers import Observer

class FileChangeHandler:
	def dispatch(self, event):
		print event

if __name__ == '__main__':
	path = sys.argv[1] if len(sys.argv[1]) > 1 else '.'
	observer = Observer()
	event_handler = FileChangeHandler()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()
