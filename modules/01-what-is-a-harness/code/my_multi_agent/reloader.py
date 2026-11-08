# reloader.py  (or fold into main.py)
import os, sys, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartOnSave(FileSystemEventHandler):
    def __init__(self):
        self._last = 0.0
    def on_modified(self, event):
        if not event.src_path.endswith((".py", ".md", ".sql")):
            return
        if ".venv" in event.src_path:            # never reload on a venv change
            return
        now = time.time()
        if now - self._last > 0.5:                 # debounce a save
            self._last = now
            print("\n[reloader] change detected — restarting…", flush=True)
            env = os.environ.copy()
            env["ADK_RELOADED"] = "1"              # tell the next process to auto-resume
            os.execve(sys.executable, [sys.executable, *sys.argv], env)   # restart IN PLACE

def start_reloader():
    observer = Observer()
    observer.schedule(RestartOnSave(), ".", recursive=True)
    observer.start()
    return observer