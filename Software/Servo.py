import serial
import time

# Configure serial communication with Arduino
try:
    arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
    print("Arduino connected")
except Exception as e:
    print(f"Arduino connection error: {e}")
    arduino = None

def send_to_arduino(command):
    try:
        if arduino and arduino.is_open:
            arduino.write(f"{command}\n".encode())
            time.sleep(0.1)  # Small delay for Arduino to process
    except Exception as e:
        print(f"Arduino write error: {e}")