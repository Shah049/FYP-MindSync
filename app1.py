from flask import Flask, jsonify
import threading
import time
import requests

app = Flask(__name__)

# ESP32 endpoint
ESP_IP = "http://192.168.39.220:8080"

# Hardcoded device-command dictionary
device_states = {
    "fan": "on",
    "light": "on"
}

def send_dict():
    while True:
        try:
            print("Sending dictionary:", device_states)
            requests.post(f"{ESP_IP}/json", json=device_states, timeout=5)
        except Exception as e:
            print("Error:", e)
        time.sleep(3)

@app.route('/')
def home():
    return jsonify({"status": "Sending device state to ESP32", "data": device_states})

# Background sender
threading.Thread(target=send_dict, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
