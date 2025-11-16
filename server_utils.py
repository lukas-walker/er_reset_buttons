import os
import signal
import time

PID_FILE = "/tmp/server_8000.pid"

def ensure_pid_file_is_usable():
    """Remove PID file if it's stale, unreadable, or belongs to dead process."""
    if not os.path.exists(PID_FILE):
        return  # no file → nothing to clean

    # Check file permissions (e.g., root-owned)
    if not os.access(PID_FILE, os.R_OK | os.W_OK):
        print(f"PID file {PID_FILE} not accessible. Removing it.")
        try:
            os.remove(PID_FILE)
        except:
            pass
        return

    # Try reading PID
    try:
        with open(PID_FILE, "r") as f:
            old_pid = int(f.read().strip())
    except:
        print("PID file unreadable or corrupt. Removing it.")
        try:
            os.remove(PID_FILE)
        except:
            pass
        return

    # Check if process is alive
    try:
        os.kill(old_pid, 0)  # check if running
    except OSError:
        print(f"Stale PID file (PID {old_pid} not running). Removing.")
        try:
            os.remove(PID_FILE)
        except:
            pass
        return

    # If it IS alive → kill it
    print(f"Killing existing server with PID {old_pid}")
    try:
        os.kill(old_pid, signal.SIGTERM)
        time.sleep(1)
    except:
        pass

def write_pid_file():
    pid = os.getpid()
    with open(PID_FILE, "w") as f:
        f.write(str(pid))
    print(f"PID file written: {PID_FILE} (PID={pid})")