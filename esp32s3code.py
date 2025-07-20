from machine import UART
import time

# UART1 (RX=GPIO44, TX=GPIO43)
uart = UART(1, baudrate=115200, tx=43, rx=44)

print("🔄 Listening for UART data from DevKit V1...")

while True:
    try:
        if uart.any():
            line = uart.readline()
            if line:
                parts = line.decode().strip().split(",")
                if len(parts) == 6:
                    alpha, beta, gamma, theta, delta, label = parts
                    print(f"🧠 EEG Data - Alpha: {alpha}, Beta: {beta}, Gamma: {gamma}, Theta: {theta}, Delta: {delta}, Label: {label}")
    except Exception as e:
        print(f"❌ UART Error: {e}")
    time.sleep(0.1)