from gpiozero import Button
import requests
import time
import server_utils

BASE_URL = "http://raspberrypi.local:8000"

server_utils.ensure_pid_file_is_usable()
server_utils.write_pid_file()

# Setup buttons with internal pull-ups
btn_reset = Button(17, pull_up=False, bounce_time=0.1)
btn_reboot = Button(27, pull_up=False, bounce_time=0.1)
btn_shutdown = Button(22, pull_up=False, bounce_time=0.1)

def do_reset():
    print("Reset button pressed")
    try:
        requests.post(f"{BASE_URL}/reset", timeout=3)
    except Exception as e:
        print("Error:", e)

def do_reboot():
    print("Reboot button pressed")
    try:
        requests.post(f"{BASE_URL}/reboot", timeout=3)
    except Exception as e:
        print("Error:", e)

def do_shutdown():
    print("Shutdown button pressed")
    try:
        requests.post(f"{BASE_URL}/shutdown", timeout=3)
    except Exception as e:
        print("Error:", e)

# Assign callbacks
btn_reset.when_pressed = do_reset
btn_reboot.when_pressed = do_reboot
btn_shutdown.when_pressed = do_shutdown

print("Physical control buttons ready...")

# Keep program alive
while True:
    time.sleep(1)