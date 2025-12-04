import threading
import datetime

class DebugLogger:
    def __init__(self, filename="debug_log.txt", enabled=True):
        self.filename = filename
        self.enabled = enabled
        self.lock = threading.Lock()

    def _write(self, level, message):
        if not self.enabled:
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_line = f"[{timestamp}] [{level}] {message}\n"
        with self.lock:
            with open(self.filename, "a") as f:
                f.write(log_line)

    def debug(self, message):
        self._write("DEBUG", message)

    def info(self, message):
        self._write("INFO", message)

    def warning(self, message):
        self._write("WARNING", message)

    def error(self, message):
        self._write("ERROR", message)

# for easy import/use
log = DebugLogger()
