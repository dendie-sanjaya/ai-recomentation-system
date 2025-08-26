import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class CSVHandler(FileSystemEventHandler):
    """Handles file system events for the data-training.csv file."""
    def on_modified(self, event):
        """Called when a file is modified."""
        if not event.is_directory and event.src_path.endswith('data-training.csv'):
            print(f"File {event.src_path} has been modified. Starting training process...")
            subprocess.run(["python", "training.py"])

if __name__ == "__main__":
    path = '.' # Direktori yang akan dipantau
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    print("Watchdog is running...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()