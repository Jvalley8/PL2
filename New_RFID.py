import serial
import time

ser = serial.Serial("/dev/ttyS0", baudrate=115200)

def read_tag():
    ser.write(bytearray.fromhex("B000000A0F01049500000000")) # Send command to read tag
    response = ser.read(64) # Read response from reader
    if response[0] == 0xB0 and response[1] == 0x00: # Check if response is valid
        tag_data = response[5:-2].hex().upper()
        print("Tag data: " + tag_data)
    else:
        print("Error reading tag")

while True:
    input("Press Enter to read tag...")
    read_tag()
    time.sleep(1)
