import network
import socket
import ujson
from machine import Pin
import time

# Wi-Fi credentials
SSID = 'Redmi12C'
PASSWORD = 'SHAHEER2002'

# Setup relays (active LOW logic)
relay1 = Pin(2, Pin.OUT)  # Fan
relay2 = Pin(3, Pin.OUT)
relay3 = Pin(4, Pin.OUT)
relay4 = Pin(5, Pin.OUT)  # Light

relays = [relay1, relay2, relay3, relay4]

# Set all relays OFF (active LOW, so HIGH means off)
def all_relays_off():
    for r in relays:
        r.value(1)

def apply_device_states(states):
    print("Received states:", states)
    all_relays_off()  # reset to OFF

    if states.get("fan") == "on":
        relay1.value(1)  # ON
    elif states.get("fan") == "off":
        relay1.value(0)

    if states.get("light") == "on":
        relay4.value(1)
    elif states.get("light") == "off":
        relay4.value(0)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to WiFi, IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Start simple web server
def start_server(ip):
    addr = socket.getaddrinfo(ip, 8080)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("ESP32 ready at http://%s:8080" % ip)

    while True:
        cl, addr = s.accept()
        print("Client connected:", addr)
        req = cl.recv(1024).decode()

        if "POST /json" in req:
            try:
                json_start = req.find('{')
                json_data = req[json_start:]
                states = ujson.loads(json_data)
                apply_device_states(states)
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nJSON processed"
            except Exception as e:
                print("JSON error:", e)
                response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"
        else:
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nESP32 Relay Controller"

        cl.send(response)
        cl.close()

# MAIN
ip = connect_wifi()
all_relays_off()
start_server(ip)
