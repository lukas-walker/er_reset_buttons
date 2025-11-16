from fastapi import FastAPI
import requests
import time
import threading
import uvicorn

import server_utils
import subprocess


# Kill old instances of this process. MAKE SURE YOU CHOOSE A UNIQUE NAME!!!!!
PID_FILE = "/tmp/client_9999.pid"

SERVER_URL = "http://raspberrypi.local:8000/state"

app = FastAPI()
game_state = {"round": 1}

def poll_server():
    global game_state
    while True:
        try:
            resp = requests.get(SERVER_URL, timeout=0.5)
            game_state = resp.json()

            if game_state.get("action") == "shutdown":
                subprocess.run(["sudo", "shutdown", "now"])

            if game_state.get("action") == "reboot":
                subprocess.run(["sudo", "reboot"])
        except:
            pass  # keep old state
        time.sleep(1)  # poll every 1 second

@app.get("/state")
def get_state():
    return game_state

if __name__ == "__main__":
    server_utils.ensure_pid_file_is_usable(PID_FILE)
    server_utils.write_pid_file(PID_FILE)

    # start polling thread
    t = threading.Thread(target=poll_server, daemon=True)
    t.start()

    # serve local HTTP API
    uvicorn.run(app, host="127.0.0.1", port=9999)