import time
import os
import threading
from pynput import mouse, keyboard
import mss
import mss.tools
import psutil
import requests
from requests.auth import HTTPBasicAuth
import json
try:
    import win32gui
    import win32process
    WINDOWS = True
except ImportError:
    WINDOWS = False

API_URL = os.getenv("API_URL", "http://localhost:8000")
USERNAME = os.getenv("AGENT_USERNAME", "testuser")
PASSWORD = os.getenv("AGENT_PASSWORD", "testpass")

class MonitorAgent:
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.key_strokes = ""
        self.last_capture_time = time.time()
        self.capture_interval = 10 # seconds
        self.token = None
        self.sct = mss.mss()

    def get_token(self):
        try:
           # Attempt to register first just in case
           requests.post(f"{API_URL}/auth/register", json={"username": USERNAME, "password": PASSWORD})
           # Login
           response = requests.post(f"{API_URL}/auth/login", data={"username": USERNAME, "password": PASSWORD})
           if response.status_code == 200:
               self.token = response.json().get("access_token")
               print("Successfully authenticated.")
           else:
               print(f"Failed to authenticate: {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")

    def get_active_window_info(self):
        app_name = "unknown"
        app_type = "unknown"
        try:
            if WINDOWS:
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                app_name = win32gui.GetWindowText(hwnd)
                process = psutil.Process(pid)
                app_type = process.name()
        except BaseException:
            pass
        return app_name, app_type

    def on_move(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.trigger_capture("mouse_click")

    def on_press(self, key):
        try:
            self.key_strokes += key.char
        except AttributeError:
            self.key_strokes += f" [{key}] "
            if key == keyboard.Key.enter:
                self.trigger_capture("enter_key")

    def trigger_capture(self, reason="interval"):
        current_time = time.time()
        
        # Debounce to prevent too many screenshots
        if current_time - self.last_capture_time < 2 and reason != "interval":
            return
            
        self.last_capture_time = current_time
        threading.Thread(target=self._capture_and_upload, args=(reason,)).start()

    def _capture_and_upload(self, reason):
        if not self.token:
            self.get_token()
            if not self.token:
                return

        try:
            # Capture screenshot
            monitor = self.sct.monitors[1]
            sct_img = self.sct.grab(monitor)
            image_path = "temp_screenshot.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=image_path)
            
            app_name, app_type = self.get_active_window_info()
            
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {
                "app_name": app_name,
                "app_type": app_type,
                "mouse_x": self.mouse_x,
                "mouse_y": self.mouse_y,
                "key_strokes": self.key_strokes
            }
            
            with open(image_path, "rb") as f:
                files = {"file": ("screenshot.png", f, "image/png")}
                res = requests.post(f"{API_URL}/agent/log", headers=headers, data=data, files=files)
                if res.status_code == 200:
                    print(f"Uploaded log successfully [{reason}]: {res.json().get('id')}")
                else:
                    print(f"Upload failed: {res.text}")
                    
            # Reset keystrokes after successful upload
            self.key_strokes = ""
        except Exception as e:
            print(f"Capture error: {e}")

    def start(self):
        print("Starting Monitor Agent...")
        self.get_token()
        
        # Start listeners
        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        try:
            while True:
                time.sleep(self.capture_interval)
                self.trigger_capture("interval")
        except KeyboardInterrupt:
            mouse_listener.stop()
            keyboard_listener.stop()
            print("Agent stopped.")

if __name__ == "__main__":
    agent = MonitorAgent()
    agent.start()
