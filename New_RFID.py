import serial
import RPi.GPIO as GPIO
import time

# Set up GPIO UART pins
TX_PIN = 14
RX_PIN = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN)

# Open serial port
ser = serial.Serial(
    port="/dev/serial0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

# Wait for reader to initialize
time.sleep(2)

# Write tag
tag_id = "123456789ABCDEF012345678"
tag_data = "Hello, world!"
write_cmd = f"WRITE_TAG_EPC_DATA {tag_id} {tag_data}\n".encode()
ser.write(write_cmd)
response = ser.readline()
print(response.decode())

# Close serial port
ser.close()
