
import serial
import RPi.GPIO as GPIO

# Set up the serial connection
ser = serial.Serial(
    port='/dev/serial0', # serial port connected to the M6E Nano reader
    baudrate=115200,     # baud rate for the serial connection
    timeout=1            # timeout for the serial read
)

# Set up the GPIO pins for the M6E Nano reader
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # GPIO 18 controls the M6E Nano's EN pin
GPIO.output(18, GPIO.HIGH)  # enable the M6E Nano

# Send the command to read a tag
ser.write(bytes.fromhex('A000300B9163960080')) # EPC Gen2 Read Tag Command

# Read the response from the M6E Nano
response = ser.read(128)

# Print the response
print(response)

# Disable the M6E Nano
GPIO.output(18, GPIO.LOW)
