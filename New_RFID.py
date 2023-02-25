import RPi.GPIO as GPIO
import serial
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Set up serial port
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

# Send write command
ser.write(bytes.fromhex('B00103000000002A3C94'))

# Wait for user prompt to put tag in range
input("Please place tag in range, then press Enter to continue...")

# Enable write pin
GPIO.output(18, GPIO.HIGH)

# Wait for write pin to stabilize
time.sleep(0.1)

# Disable write pin
GPIO.output(18, GPIO.LOW)

# Wait for write to complete
time.sleep(0.5)

# Disable read pin
GPIO.output(23, GPIO.LOW)

# Close serial port
ser.close()

